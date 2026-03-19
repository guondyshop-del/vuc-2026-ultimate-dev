#!/bin/bash

# VUC-2026 Production Deployment Script
# Automated deployment with health checks and rollback

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="vuc-2026"
ENVIRONMENT="production"
BACKUP_DIR="/opt/backups/vuc-2026"
LOG_FILE="/var/log/vuc-2026-deploy.log"
HEALTH_CHECK_TIMEOUT=300
ROLLBACK_ON_FAILURE=true

# Function to log messages
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check Docker
    if ! command_exists docker; then
        error "Docker is not installed"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command_exists docker-compose; then
        error "Docker Compose is not installed"
        exit 1
    fi
    
    # Check if .env file exists
    if [ ! -f ".env.prod" ]; then
        error "Environment file .env.prod not found"
        exit 1
    fi
    
    # Check if SSL certificates exist
    if [ ! -d "nginx/ssl" ]; then
        warning "SSL certificates directory not found. Creating self-signed certificates..."
        mkdir -p nginx/ssl
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout nginx/ssl/vuc-2026.com.key \
            -out nginx/ssl/vuc-2026.com.crt \
            -subj "/C=TR/ST=ISTANBUL/L=ISTANBUL/O=VUC-2026/OU=IT/CN=vuc-2026.com"
    fi
    
    success "Prerequisites check completed"
}

# Function to create backup
create_backup() {
    log "Creating backup..."
    
    BACKUP_NAME="${PROJECT_NAME}-backup-$(date +%Y%m%d-%H%M%S)"
    BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"
    
    mkdir -p "$BACKUP_PATH"
    
    # Backup database
    docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U vuc_user vuc2026_prod > "${BACKUP_PATH}/database.sql"
    
    # Backup volumes
    docker run --rm -v vuc-2026_postgres_data:/data -v "${BACKUP_PATH}:/backup" alpine tar czf /backup/postgres_data.tar.gz -C /data .
    docker run --rm -v vuc-2026_redis_data:/data -v "${BACKUP_PATH}:/backup" alpine tar czf /backup/redis_data.tar.gz -C /data .
    
    # Backup configuration
    cp -r nginx "${BACKUP_PATH}/"
    cp .env.prod "${BACKUP_PATH}/"
    
    success "Backup created: ${BACKUP_PATH}"
    echo "${BACKUP_PATH}" > "${BACKUP_DIR}/last_backup.txt"
}

# Function to pull latest images
pull_images() {
    log "Pulling latest Docker images..."
    
    docker-compose -f docker-compose.prod.yml pull
    
    success "Images pulled successfully"
}

# Function to build custom images
build_images() {
    log "Building custom Docker images..."
    
    docker-compose -f docker-compose.prod.yml build --no-cache
    
    success "Images built successfully"
}

# Function to run database migrations
run_migrations() {
    log "Running database migrations..."
    
    docker-compose -f docker-compose.prod.yml run --rm backend alembic upgrade head
    
    success "Database migrations completed"
}

# Function to deploy services
deploy_services() {
    log "Deploying services..."
    
    # Stop existing services
    docker-compose -f docker-compose.prod.yml down
    
    # Start services
    docker-compose -f docker-compose.prod.yml up -d
    
    success "Services deployed"
}

# Function to health check
health_check() {
    log "Performing health checks..."
    
    local services=("backend:8000" "frontend:3000" "postgres:5432" "redis:6379")
    local healthy=true
    
    for service in "${services[@]}"; do
        local name=$(echo "$service" | cut -d':' -f1)
        local port=$(echo "$service" | cut -d':' -f2)
        local timeout=0
        
        log "Checking ${name} health..."
        
        while [ $timeout -lt $HEALTH_CHECK_TIMEOUT ]; do
            if docker-compose -f docker-compose.prod.yml exec -T "$name" /bin/sh -c "nc -z localhost $port" 2>/dev/null; then
                success "${name} is healthy"
                break
            fi
            
            sleep 5
            timeout=$((timeout + 5))
        done
        
        if [ $timeout -ge $HEALTH_CHECK_TIMEOUT ]; then
            error "${name} health check failed after ${HEALTH_CHECK_TIMEOUT} seconds"
            healthy=false
        fi
    done
    
    if [ "$healthy" = false ]; then
        error "Health checks failed"
        return 1
    fi
    
    success "All health checks passed"
    return 0
}

# Function to rollback
rollback() {
    log "Rolling back deployment..."
    
    if [ ! -f "${BACKUP_DIR}/last_backup.txt" ]; then
        error "No backup found for rollback"
        exit 1
    fi
    
    BACKUP_PATH=$(cat "${BACKUP_DIR}/last_backup.txt")
    
    # Stop current services
    docker-compose -f docker-compose.prod.yml down
    
    # Restore database
    docker-compose -f docker-compose.prod.yml up -d postgres
    sleep 30
    docker-compose -f docker-compose.prod.yml exec -T postgres psql -U vuc_user -c "DROP DATABASE IF EXISTS vuc2026_prod;"
    docker-compose -f docker-compose.prod.yml exec -T postgres psql -U vuc_user -c "CREATE DATABASE vuc2026_prod;"
    docker-compose -f docker-compose.prod.yml exec -T postgres psql -U vuc_user vuc2026_prod < "${BACKUP_PATH}/database.sql"
    
    # Restore volumes
    docker run --rm -v vuc-2026_postgres_data:/data -v "${BACKUP_PATH}:/backup" alpine tar xzf /backup/postgres_data.tar.gz -C /data
    docker run --rm -v vuc-2026_redis_data:/data -v "${BACKUP_PATH}:/backup" alpine tar xzf /backup/redis_data.tar.gz -C /data
    
    # Restore configuration
    cp -r "${BACKUP_PATH}/nginx" ./
    cp "${BACKUP_PATH}/.env.prod" ./
    
    # Start all services
    docker-compose -f docker-compose.prod.yml up -d
    
    success "Rollback completed"
}

# Function to cleanup old images and containers
cleanup() {
    log "Cleaning up old Docker resources..."
    
    # Remove unused images
    docker image prune -f
    
    # Remove unused containers
    docker container prune -f
    
    # Remove unused networks
    docker network prune -f
    
    success "Cleanup completed"
}

# Function to show deployment status
show_status() {
    log "Deployment status:"
    
    docker-compose -f docker-compose.prod.yml ps
    
    echo ""
    log "Resource usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
}

# Main deployment function
deploy() {
    log "Starting VUC-2026 deployment..."
    
    # Create backup
    create_backup
    
    # Check prerequisites
    check_prerequisites
    
    # Pull latest images
    pull_images
    
    # Build custom images
    build_images
    
    # Deploy services
    deploy_services
    
    # Wait for services to start
    log "Waiting for services to start..."
    sleep 30
    
    # Run migrations
    run_migrations
    
    # Health check
    if health_check; then
        success "Deployment completed successfully!"
        show_status
    else
        error "Deployment failed health checks"
        
        if [ "$ROLLBACK_ON_FAILURE" = true ]; then
            warning "Rolling back to previous version..."
            rollback
        fi
        
        exit 1
    fi
    
    # Cleanup
    cleanup
}

# Function to show usage
usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy      Deploy the application"
    echo "  rollback    Rollback to previous version"
    echo "  status      Show deployment status"
    echo "  backup      Create backup"
    echo "  health      Run health checks"
    echo "  cleanup     Cleanup Docker resources"
    echo ""
    echo "Examples:"
    echo "  $0 deploy"
    echo "  $0 rollback"
    echo "  $0 status"
}

# Parse command line arguments
case "${1:-deploy}" in
    deploy)
        deploy
        ;;
    rollback)
        rollback
        ;;
    status)
        show_status
        ;;
    backup)
        create_backup
        ;;
    health)
        health_check
        ;;
    cleanup)
        cleanup
        ;;
    *)
        usage
        exit 1
        ;;
esac
