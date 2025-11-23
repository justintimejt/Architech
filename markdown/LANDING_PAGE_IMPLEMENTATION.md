# Landing Page Implementation Guide

## Overview
This document outlines the implementation of the landing page with the dot-shader background component, following the specifications in `LANDING_PAGE_OUTLINE.md`.

## Components Created

### 1. Theme Context (`frontend/src/contexts/ThemeContext.tsx`)
A React context provider for managing theme state (light/dark mode).
- Persists theme preference to localStorage
- Falls back to system preference if no saved theme
- Applies theme class to document root
- Exports `useTheme` hook for components

**Usage:**
```tsx
import { useTheme } from '../../contexts/ThemeContext';

const { theme, toggleTheme, setTheme } = useTheme();
```

### 2. Dot Shader Background (`frontend/src/components/ui/dot-shader-background.tsx`)
An animated Three.js shader component that creates an interactive dot grid background.
- Responds to mouse movement with trail effects
- Theme-aware (adapts colors based on light/dark mode)
- Uses the blue/black color palette from the design
- GPU-accelerated for smooth performance

**Features:**
- Animated dots that scale and rotate
- Mouse trail interaction
- Smooth color transitions
- Responsive to viewport size

**Usage:**
```tsx
import { DotScreenShader } from '@/components/ui/dot-shader-background';

<div className="absolute inset-0">
  <DotScreenShader />
</div>
```

### 3. Demo Component (`frontend/src/components/ui/dot-shader-demo.tsx`)
Example implementation showing how to use the dot-shader background with text overlay.

## Dependencies

### Already Installed ✅
- `three` (^0.169.0)
- `@react-three/fiber` (^8.18.0)
- `@react-three/drei` (^9.122.0)
- `lucide-react` (^0.554.0) - for icons
- `tailwindcss` (^3.3.6)
- `typescript` (^5.2.2)

### No Additional Dependencies Needed
The component has been adapted to work without `next-themes` by using a custom `ThemeContext` provider.

## Setup Instructions

### 1. Theme Provider Setup
The `ThemeProvider` has been added to `main.tsx`. The app is now wrapped with the theme provider, so all components can access theme state.

### 2. Component Integration
The dot-shader component is exported from `frontend/src/components/ui/index.ts` and can be imported using:
```tsx
import { DotScreenShader } from '@/components/ui';
// or
import { DotScreenShader } from '@/components/ui/dot-shader-background';
```

### 3. Color Palette Integration
The component uses the following colors from the design palette:
- **Dark Mode:**
  - Background: `#1B2631` (Dark Blue/Charcoal)
  - Dots: `#FFFFFF` (White)
- **Light Mode:**
  - Background: `#F7F7F7` (Off-White)
  - Dots: `#4A90E2` (Vibrant Blue)

## Next Steps for Landing Page Implementation

### 1. Update HomePage Component
Modify `frontend/src/pages/HomePage.tsx` to:
- Add the `DotScreenShader` background
- Implement the hero section with CTAs
- Add smooth scroll functionality
- Use the blue/black color scheme

### 2. Create Additional Sections
Following the outline in `LANDING_PAGE_OUTLINE.md`:
- Features section with cards
- Video demonstration section
- Testimonials (optional)
- Final CTA section
- Footer

### 3. Add Animations
Consider adding:
- `framer-motion` for scroll animations (optional)
- CSS transitions for hover effects
- Smooth scroll behavior

### 4. Responsive Design
Ensure all sections are responsive:
- Mobile-first approach
- Breakpoints: 768px (tablet), 1024px (desktop)
- Test on various screen sizes

## Example Landing Page Structure

```tsx
import { DotScreenShader } from '@/components/ui';
import { useNavigate } from 'react-router-dom';

export function HomePage() {
  const navigate = useNavigate();

  const scrollToVideo = () => {
    const videoSection = document.getElementById('video-section');
    videoSection?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen relative">
      {/* Hero Section with Dot Shader */}
      <section className="h-screen relative flex items-center justify-center">
        <div className="absolute inset-0">
          <DotScreenShader />
        </div>
        <div className="relative z-10 text-center">
          <h1 className="text-6xl md:text-7xl font-light text-white mix-blend-exclusion">
            Turn Ideas into Stunning Architecture Diagrams
          </h1>
          <div className="mt-8 flex gap-4 justify-center">
            <button onClick={() => navigate('/login')}>
              Get Started
            </button>
            <button onClick={scrollToVideo}>
              See It In Action
            </button>
          </div>
        </div>
      </section>

      {/* Video Section */}
      <section id="video-section" className="min-h-screen bg-[#1B2631]">
        {/* Video content */}
      </section>
    </div>
  );
}
```

## Styling Guidelines

### Color Usage
- **Primary Dark**: `#1B2631` - Main dark backgrounds
- **Primary Blue**: `#4A90E2` - CTAs, accents, interactive elements
- **Secondary Blue**: `#2C3E50` - Secondary backgrounds
- **Light Blue**: `#A2DFF7` - Highlights, hover states
- **Off-White**: `#F7F7F7` - Light backgrounds
- **Light Gray**: `#D5D5D5` - Borders, dividers

### Typography
- Use `mix-blend-exclusion` for text over the dot-shader background
- Large, bold headlines (4xl-7xl)
- Light weight for body text
- White/light colors for dark backgrounds

### Spacing
- Generous padding and margins
- Consistent spacing scale
- Responsive spacing (smaller on mobile)

## Performance Considerations

1. **Lazy Loading**: Consider lazy loading the video section
2. **Shader Performance**: The dot-shader is GPU-accelerated but monitor performance on lower-end devices
3. **Image Optimization**: Use optimized images for feature cards
4. **Code Splitting**: Consider code splitting for the landing page

## Accessibility

- Ensure all interactive elements have proper ARIA labels
- Maintain keyboard navigation
- Test with screen readers
- Ensure sufficient color contrast
- Provide focus indicators

## Testing Checklist

- [ ] Dot-shader renders correctly
- [ ] Theme switching works
- [ ] Mouse interaction works on shader
- [ ] Smooth scrolling functions
- [ ] Buttons navigate correctly
- [ ] Responsive on mobile/tablet/desktop
- [ ] Video section loads properly
- [ ] All animations are smooth
- [ ] Accessibility features work
- [ ] Performance is acceptable

## Troubleshooting

### Issue: Dot-shader not rendering
- Check that Three.js dependencies are installed
- Verify Canvas is properly mounted
- Check browser console for errors

### Issue: Theme not persisting
- Check localStorage permissions
- Verify ThemeProvider is wrapping the app
- Check that theme class is being applied to root

### Issue: Performance issues
- Reduce gridSize in dot-shader component
- Lower the resolution of the shader
- Consider disabling mouse trail on mobile

