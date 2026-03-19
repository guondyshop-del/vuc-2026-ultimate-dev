# VUC-2026 Frontend

Enterprise-grade Next.js frontend for the VUC-2026 autonomous YouTube content production system.

## 🚀 Features

### Core Functionality
- **Real-time Dashboard**: Live job tracking and system metrics
- **Job Management**: Create, monitor, and manage video production jobs
- **Pipeline Tracking**: Real-time progress visualization
- **Analytics Dashboard**: Performance metrics and insights
- **Responsive Design**: Mobile-first approach with desktop optimization

### Technical Stack
- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS with custom VUC-2026 design system
- **Components**: Reusable React components with TypeScript
- **State Management**: React hooks and context
- **API Client**: Axios with interceptors and error handling
- **Forms**: React Hook Form with Zod validation
- **Animations**: Framer Motion for smooth transitions
- **Icons**: Lucide React icon library
- **Notifications**: React Hot Toast

### UI/UX Features
- **Modern Design**: Clean, professional interface
- **Dark Mode Support**: Automatic theme detection
- **Accessibility**: WCAG 2.1 compliant components
- **Performance**: Optimized for fast loading
- **SEO**: Meta tags and structured data
- **Internationalization**: Turkish language support

## 📦 Installation

```bash
# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Start development server
npm run dev
```

## 🔧 Environment Variables

Create a `.env.local` file in the root directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=VUC-2026 Enterprise
NEXT_PUBLIC_APP_VERSION=1.0.0
```

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── globals.css     # Global styles
│   │   ├── layout.tsx       # Root layout
│   │   └── page.tsx         # Main dashboard
│   ├── components/          # Reusable components
│   │   ├── JobCreator.tsx   # Job creation form
│   │   ├── PipelineTracker.tsx # Progress tracking
│   │   └── ...              # Other components
│   ├── lib/                 # Utilities
│   │   └── api.ts           # API client
│   └── types/               # TypeScript types
├── public/                  # Static assets
├── tailwind.config.ts       # Tailwind configuration
├── next.config.js           # Next.js configuration
└── package.json             # Dependencies
```

## 🎨 Design System

### Colors
- **Primary**: Blue (#3b82f6)
- **Secondary**: Purple (#d946ef)
- **Success**: Green (#22c55e)
- **Warning**: Yellow (#f59e0b)
- **Danger**: Red (#ef4444)
- **Dark**: Gray (#1e293b)

### Typography
- **Font Family**: Inter
- **Headings**: Display font weight (700)
- **Body**: Regular font weight (400)
- **Small**: Light font weight (300)

### Components
- **Buttons**: Multiple variants (primary, secondary, outline)
- **Cards**: Consistent shadow and border radius
- **Forms**: Validation and error states
- **Modals**: Overlay and content styling
- **Tables**: Responsive and sortable

## 🚀 Development

### Available Scripts

```bash
# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linting
npm run lint

# Fix linting issues
npm run lint:fix

# Type checking
npm run type-check

# Export static files
npm run export
```

### Code Quality

- **ESLint**: Configured for Next.js and TypeScript
- **Prettier**: Code formatting
- **TypeScript**: Strict mode enabled
- **Git Hooks**: Pre-commit linting

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

### Mobile Optimizations
- Touch-friendly controls
- Optimized navigation
- Responsive tables
- Mobile-first approach

## 🔐 Security

### Headers
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- Referrer-Policy: origin-when-cross-origin

### Best Practices
- Input validation
- XSS prevention
- CSRF protection
- Secure API communication

## 📊 Performance

### Optimization
- Image optimization with Next.js
- Code splitting
- Lazy loading
- Minification
- Caching strategies

### Metrics
- **Lighthouse Score**: 95+
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1

## 🌐 API Integration

### Endpoints
- `/api/jobs` - Job management
- `/api/health` - System health
- `/api/metrics` - Performance metrics

### Error Handling
- Global error boundaries
- API error interceptors
- User-friendly error messages
- Retry mechanisms

## 🎯 Features

### Dashboard
- Real-time job status
- System metrics
- Quick actions
- Recent activity

### Job Management
- Multi-step job creation
- Progress tracking
- Status updates
- Error handling

### Analytics
- Performance metrics
- Success rates
- Processing times
- Resource usage

## 🔧 Configuration

### Tailwind CSS
- Custom design tokens
- Component utilities
- Responsive utilities
- Animation classes

### Next.js
- App Router
- Server components
- Client components
- API routes

## 📚 Documentation

### Components
- Prop types with TypeScript
- Usage examples
- Best practices
- Accessibility notes

### API
- Request/response types
- Error handling
- Authentication
- Rate limiting

## 🚀 Deployment

### Build Process
```bash
# Build for production
npm run build

# Start production server
npm start
```

### Environment
- Development: `npm run dev`
- Staging: Environment-specific
- Production: Optimized build

## 🤝 Contributing

### Guidelines
- Follow existing code style
- Add TypeScript types
- Include tests
- Update documentation

### Code Review
- PR template
- Review checklist
- Approval process

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

### Issues
- Bug reports
- Feature requests
- Documentation issues
- Security concerns

### Contact
- Development team
- Project maintainers
- Community support
