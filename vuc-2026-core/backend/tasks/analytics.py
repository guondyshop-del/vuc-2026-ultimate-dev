"""
VUC-2026 Analytics Tasks
Celery tasks for analytics collection and reporting
"""

import asyncio
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, and_, or_

from ..core.database import AsyncSessionLocal
from ..core.logger import get_logger, VUCLogger
from ..models.video_job import VideoJobRepository

logger = get_logger(__name__)
vuc_logger = VUCLogger()


async def collect_daily_analytics():
    """
    Collect daily analytics data
    """
    analytics_data = {
        "date": datetime.now(timezone.utc).date().isoformat(),
        "metrics": {},
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    try:
        async with AsyncSessionLocal() as session:
            repo = VideoJobRepository(session)
            
            # Get jobs from last 24 hours
            yesterday = datetime.now(timezone.utc) - timedelta(days=1)
            
            # Total jobs created
            all_jobs = await repo.list_jobs(limit=1000)
            recent_jobs = [job for job in all_jobs if job.created_at >= yesterday]
            
            analytics_data["metrics"]["jobs_created_today"] = len(recent_jobs)
            
            # Jobs by status
            status_counts = {}
            for job in recent_jobs:
                status_counts[job.status] = status_counts.get(job.status, 0) + 1
            
            analytics_data["metrics"]["jobs_by_status"] = status_counts
            
            # Completed jobs metrics
            completed_jobs = [job for job in recent_jobs if job.status == "completed"]
            
            if completed_jobs:
                # Average processing time
                processing_times = [job.processing_duration for job in completed_jobs if job.processing_duration]
                avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
                
                analytics_data["metrics"]["avg_processing_time_minutes"] = avg_processing_time / 60
                
                # Average video duration
                video_durations = [job.video_duration for job in completed_jobs if job.video_duration]
                avg_video_duration = sum(video_durations) / len(video_durations) if video_durations else 0
                
                analytics_data["metrics"]["avg_video_duration_seconds"] = avg_video_duration
                
                # Total video size
                total_size = sum(job.video_size for job in completed_jobs if job.video_size)
                analytics_data["metrics"]["total_video_size_mb"] = total_size / (1024 * 1024)
                
                # Quality distribution
                quality_counts = {}
                for job in completed_jobs:
                    if job.video_quality:
                        quality_counts[job.video_quality] = quality_counts.get(job.video_quality, 0) + 1
                
                analytics_data["metrics"]["video_quality_distribution"] = quality_counts
            
            # Failed jobs analysis
            failed_jobs = [job for job in recent_jobs if job.status == "failed"]
            
            if failed_jobs:
                # Common error patterns
                error_messages = [job.error_message for job in failed_jobs if job.error_message]
                error_patterns = {}
                
                for error in error_messages:
                    # Simple pattern matching
                    if "timeout" in error.lower():
                        error_patterns["timeout"] = error_patterns.get("timeout", 0) + 1
                    elif "connection" in error.lower():
                        error_patterns["connection"] = error_patterns.get("connection", 0) + 1
                    elif "memory" in error.lower():
                        error_patterns["memory"] = error_patterns.get("memory", 0) + 1
                    else:
                        error_patterns["other"] = error_patterns.get("other", 0) + 1
                
                analytics_data["metrics"]["failure_patterns"] = error_patterns
            
            # Age group distribution
            age_groups = {}
            for job in recent_jobs:
                age_range = f"{job.target_age_min}-{job.target_age_max}"
                age_groups[age_range] = age_groups.get(age_range, 0) + 1
            
            analytics_data["metrics"]["age_group_distribution"] = age_groups
            
            # Topic popularity
            topic_counts = {}
            for job in recent_jobs:
                topic_counts[job.topic] = topic_counts.get(job.topic, 0) + 1
            
            # Sort by popularity
            sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            analytics_data["metrics"]["popular_topics"] = dict(sorted_topics)
            
            # YouTube metrics (if available)
            youtube_jobs = [job for job in completed_jobs if job.youtube_video_id]
            
            if youtube_jobs:
                total_views = sum(job.view_count for job in youtube_jobs)
                total_likes = sum(job.like_count for job in youtube_jobs)
                total_comments = sum(job.comment_count for job in youtube_jobs)
                
                analytics_data["metrics"]["youtube_total_views"] = total_views
                analytics_data["metrics"]["youtube_total_likes"] = total_likes
                analytics_data["metrics"]["youtube_total_comments"] = total_comments
                
                # Engagement rate
                if total_views > 0:
                    engagement_rate = ((total_likes + total_comments) / total_views) * 100
                    analytics_data["metrics"]["youtube_engagement_rate"] = round(engagement_rate, 2)
            
            logger.info(f"Daily analytics collected: {analytics_data['metrics']}")
            
            return analytics_data
            
    except Exception as e:
        logger.error(f"Failed to collect daily analytics: {e}")
        analytics_data["error"] = str(e)
        return analytics_data


async def generate_performance_report():
    """
    Generate comprehensive performance report
    """
    report = {
        "report_date": datetime.now(timezone.utc).date().isoformat(),
        "period": "last_7_days",
        "metrics": {},
        "recommendations": [],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    try:
        async with AsyncSessionLocal() as session:
            repo = VideoJobRepository(session)
            
            # Get jobs from last 7 days
            week_ago = datetime.now(timezone.utc) - timedelta(days=7)
            all_jobs = await repo.list_jobs(limit=1000)
            recent_jobs = [job for job in all_jobs if job.created_at >= week_ago]
            
            if not recent_jobs:
                report["metrics"]["message"] = "No jobs found in the last 7 days"
                return report
            
            # Success rate
            completed_count = len([job for job in recent_jobs if job.status == "completed"])
            failed_count = len([job for job in recent_jobs if job.status == "failed"])
            total_count = len(recent_jobs)
            
            success_rate = (completed_count / total_count) * 100 if total_count > 0 else 0
            report["metrics"]["success_rate_percent"] = round(success_rate, 2)
            
            # Processing performance
            completed_jobs = [job for job in recent_jobs if job.status == "completed" and job.processing_duration]
            
            if completed_jobs:
                processing_times = [job.processing_duration for job in completed_jobs]
                avg_processing_time = sum(processing_times) / len(processing_times)
                min_processing_time = min(processing_times)
                max_processing_time = max(processing_times)
                
                report["metrics"]["processing_performance"] = {
                    "avg_seconds": round(avg_processing_time, 2),
                    "min_seconds": round(min_processing_time, 2),
                    "max_seconds": round(max_processing_time, 2),
                    "avg_minutes": round(avg_processing_time / 60, 2)
                }
            
            # Video quality metrics
            video_jobs = [job for job in completed_jobs if job.video_duration]
            
            if video_jobs:
                durations = [job.video_duration for job in video_jobs]
                sizes = [job.video_size for job in video_jobs if job.video_size]
                
                report["metrics"]["video_quality"] = {
                    "avg_duration_seconds": round(sum(durations) / len(durations), 2),
                    "avg_size_mb": round(sum(sizes) / len(sizes) / (1024 * 1024), 2) if sizes else 0,
                    "total_videos": len(video_jobs)
                }
            
            # Error analysis
            failed_jobs = [job for job in recent_jobs if job.status == "failed"]
            
            if failed_jobs:
                error_categories = {}
                for job in failed_jobs:
                    if job.error_message:
                        error_msg = job.error_message.lower()
                        
                        if "timeout" in error_msg:
                            category = "timeout"
                        elif "memory" in error_msg:
                            category = "memory"
                        elif "connection" in error_msg:
                            category = "connection"
                        elif "api" in error_msg:
                            category = "api"
                        else:
                            category = "other"
                        
                        error_categories[category] = error_categories.get(category, 0) + 1
                
                report["metrics"]["error_categories"] = error_categories
                
                # Most common error
                if error_categories:
                    most_common = max(error_categories.items(), key=lambda x: x[1])
                    report["metrics"]["most_common_error"] = {
                        "category": most_common[0],
                        "count": most_common[1]
                    }
            
            # Generate recommendations
            recommendations = []
            
            if success_rate < 80:
                recommendations.append("Consider reviewing failed jobs to identify common issues")
            
            if completed_jobs and avg_processing_time > 600:  # 10 minutes
                recommendations.append("Processing time is high, consider optimizing the pipeline")
            
            if failed_count > completed_count:
                recommendations.append("Failure rate is high, investigate system issues")
            
            if len(video_jobs) > 0:
                avg_size = sum(job.video_size for job in video_jobs if job.video_size) / len([job for job in video_jobs if job.video_size])
                if avg_size > 500 * 1024 * 1024:  # 500MB
                    recommendations.append("Video sizes are large, consider compression")
            
            report["recommendations"] = recommendations
            
            logger.info(f"Performance report generated: {report['metrics']}")
            
            return report
            
    except Exception as e:
        logger.error(f"Failed to generate performance report: {e}")
        report["error"] = str(e)
        return report


async def update_youtube_analytics():
    """
    Update YouTube analytics for completed jobs
    """
    update_results = {
        "jobs_updated": 0,
        "total_views": 0,
        "total_likes": 0,
        "total_comments": 0,
        "errors": [],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    try:
        async with AsyncSessionLocal() as session:
            repo = VideoJobRepository(session)
            
            # Get completed jobs with YouTube videos from last 24 hours
            yesterday = datetime.now(timezone.utc) - timedelta(days=1)
            
            all_jobs = await repo.list_jobs(status="completed", limit=1000)
            recent_youtube_jobs = [
                job for job in all_jobs 
                if job.youtube_video_id and job.created_at >= yesterday
            ]
            
            # Import YouTube publisher
            from ..services.youtube_publisher import youtube_publisher
            
            for job in recent_youtube_jobs:
                try:
                    # Get video analytics
                    analytics = await youtube_publisher.get_video_analytics(job.youtube_video_id)
                    
                    # Update job with new analytics
                    await repo.update_metadata(job.job_id, {
                        "view_count": analytics["view_count"],
                        "like_count": analytics["like_count"],
                        "comment_count": analytics["comment_count"],
                        "youtube_analytics_updated": datetime.now(timezone.utc).isoformat()
                    })
                    
                    update_results["jobs_updated"] += 1
                    update_results["total_views"] += analytics["view_count"]
                    update_results["total_likes"] += analytics["like_count"]
                    update_results["total_comments"] += analytics["comment_count"]
                    
                    logger.info(f"Updated analytics for job {job.job_id}: {analytics['view_count']} views")
                    
                except Exception as e:
                    error_msg = f"Failed to update analytics for job {job.job_id}: {e}"
                    update_results["errors"].append(error_msg)
                    logger.warning(error_msg)
            
            logger.info(f"YouTube analytics update completed: {update_results['jobs_updated']} jobs updated")
            
            return update_results
            
    except Exception as e:
        logger.error(f"Failed to update YouTube analytics: {e}")
        update_results["errors"].append(f"Update failed: {e}")
        return update_results


# Celery task definitions
from ..celery_app import celery_app


@celery_app.task(name="backend.tasks.analytics.update_analytics")
def update_analytics_task():
    """
    Celery task to update analytics
    """
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Update daily analytics
        daily_result = loop.run_until_complete(collect_daily_analytics())
        
        # Store analytics (would save to database or file)
        logger.info("Daily analytics updated")
        
        return daily_result
        
    except Exception as e:
        logger.error(f"Analytics update task failed: {e}")
        raise


@celery_app.task(name="backend.tasks.analytics.generate_performance_report")
def generate_performance_report_task():
    """
    Celery task to generate performance report
    """
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        report = loop.run_until_complete(generate_performance_report())
        
        logger.info("Performance report generated")
        
        return report
        
    except Exception as e:
        logger.error(f"Performance report task failed: {e}")
        raise


@celery_app.task(name="backend.tasks.analytics.update_youtube_analytics")
def update_youtube_analytics_task():
    """
    Celery task to update YouTube analytics
    """
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(update_youtube_analytics())
        
        logger.info("YouTube analytics updated")
        
        return result
        
    except Exception as e:
        logger.error(f"YouTube analytics update task failed: {e}")
        raise
