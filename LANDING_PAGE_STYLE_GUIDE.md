# Landing Page Style Guide

## Overview
This document outlines the complete styling system used on the BuildFlow landing page. All styles follow a dark theme with black backgrounds, white text, and minimal color accents.

---

## Color Palette

### Primary Colors

#### Background Colors
- **Pure Black**: `#000000` / `bg-black`
  - Primary background color for the entire page
  - Used for main container, sections, and video container backgrounds

#### Text Colors
- **Pure White**: `#FFFFFF` / `text-white`
  - Primary text color for headings and important content
  - Used with `mix-blend-exclusion` for visibility over dot-shader background

- **White 70% Opacity**: `text-white/70`
  - Secondary text color for descriptions and body text
  - Used for subtitles and supporting content

- **White 50% Opacity**: `text-white/50`
  - Tertiary text color for less important text
  - Used for fine print, captions, and metadata

#### Accent Colors (Minimal Usage)
- **Gray 200**: `#E5E7EB` / `bg-gray-200` / `hover:bg-gray-200`
  - Hover state for primary buttons
  - Light gray for subtle hover effects

### Dot Shader Background Colors
- **Dot Color**: `#FFFFFF` (White)
  - Color of the animated dots in the shader background
  - Opacity: `0.025` (2.5%)

- **Background Color**: `#000000` (Pure Black)
  - Background color for the dot shader component

### Glassmorphism Colors
- **White 5% Opacity**: `bg-white/5`
  - Base background for glassmorphism cards
  - Creates subtle translucent effect

- **White 10% Opacity**: `bg-white/10`
  - Used for logo container and button backgrounds
  - Slightly more opaque than base

- **White 20% Opacity**: `bg-white/20` / `border-white/20`
  - Used for borders and hover states
  - Creates visible but subtle boundaries

- **White 30% Opacity**: `hover:bg-white/30`
  - Hover state for interactive elements
  - More visible on interaction

### Border Colors
- **White 10% Opacity**: `border-white/10`
  - Primary border color for cards and containers
  - Subtle separation between elements

- **White 20% Opacity**: `border-white/20`
  - Secondary border color
  - Used for logo container and icons

- **White 50% Opacity**: `border-white/50`
  - Tertiary border color for buttons
  - More visible borders for CTAs

---

## Typography

### Font Family
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
  'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
```
- System font stack for optimal performance and native feel
- Uses platform-specific fonts for best rendering

### Font Smoothing
- `-webkit-font-smoothing: antialiased`
- `-moz-osx-font-smoothing: grayscale`
- Ensures crisp text rendering across browsers

### Heading Styles

#### H1 - Logo/Brand Name
- **Size**: `text-2xl` (1.5rem / 24px)
- **Weight**: `font-bold` (700)
- **Color**: `text-white`
- **Usage**: Header logo text

#### H2 - Main Hero Headline
- **Size**: 
  - Mobile: `text-5xl` (3rem / 48px)
  - Tablet: `md:text-6xl` (3.75rem / 60px)
  - Desktop: `lg:text-7xl` (4.5rem / 72px)
- **Weight**: `font-light` (300)
- **Tracking**: `tracking-tight` (-0.025em)
- **Line Height**: `leading-tight` (1.25)
- **Color**: `text-white` with `mix-blend-exclusion`
- **Margin Bottom**: `mb-6` (1.5rem / 24px)
- **Usage**: Primary hero headline

#### H3 - Section Headings
- **Size**: 
  - Mobile: `text-4xl` (2.25rem / 36px)
  - Desktop: `md:text-5xl` (3rem / 48px)
- **Weight**: `font-light` (300)
- **Color**: `text-white`
- **Margin Bottom**: `mb-4` (1rem / 16px)
- **Usage**: Section titles (e.g., "See BuildFlow in Action")

### Body Text Styles

#### Large Body Text (Hero Description)
- **Size**: 
  - Mobile: `text-xl` (1.25rem / 20px)
  - Desktop: `md:text-2xl` (1.5rem / 24px)
- **Weight**: `font-light` (300)
- **Color**: `text-white` with `mix-blend-exclusion`
- **Line Height**: `leading-relaxed` (1.625)
- **Max Width**: `max-w-3xl` (48rem / 768px)
- **Margin Bottom**: `mb-10` (2.5rem / 40px)
- **Usage**: Hero section description

#### Standard Body Text
- **Size**: `text-xl` (1.25rem / 20px)
- **Weight**: Regular (400)
- **Color**: `text-white/70`
- **Max Width**: `max-w-2xl` (42rem / 672px)
- **Usage**: Section descriptions

#### Small Text
- **Size**: `text-sm` (0.875rem / 14px)
- **Weight**: Regular (400)
- **Color**: `text-white/50`
- **Usage**: Fine print, captions, metadata

#### Semibold Accent Text
- **Weight**: `font-semibold` (600)
- **Color**: `text-white`
- **Usage**: Emphasized words within body text

### Text Effects

#### Mix Blend Exclusion
- **Property**: `mix-blend-exclusion`
- **Usage**: Applied to text over dot-shader background
- **Effect**: Inverts colors for better visibility against animated background

---

## Spacing System

### Container Spacing

#### Page Container
- **Padding Horizontal**: `px-6` (1.5rem / 24px)
- **Padding Vertical**: `py-20` (5rem / 80px) for sections
- **Max Width**: 
  - Hero: `max-w-5xl` (64rem / 1024px)
  - Video Section: `max-w-6xl` (72rem / 1152px)
  - General: `max-w-7xl` (80rem / 1280px)

#### Section Spacing
- **Padding**: `py-20 px-6` (5rem vertical, 1.5rem horizontal)
- **Min Height**: `min-h-screen` (100vh) for full viewport sections

### Component Spacing

#### Header/Logo
- **Padding**: `px-6 py-6` (1.5rem / 24px)
- **Gap**: `gap-3` (0.75rem / 12px) between logo and text

#### Buttons
- **Padding**: 
  - Primary: `px-8 py-6` (2rem horizontal, 1.5rem vertical)
  - Large: `px-10 py-6` (2.5rem horizontal, 1.5rem vertical)
- **Gap**: `gap-4` (1rem / 16px) between buttons
- **Icon Gap**: `gap-2` (0.5rem / 8px) between text and icons

#### Cards/Containers
- **Padding**: `p-8` (2rem / 32px)
- **Border Radius**: `rounded-2xl` (1rem / 16px)
- **Margin Bottom**: `mb-12` (3rem / 48px) for video container

### Text Spacing

#### Headings
- **Margin Bottom**: 
  - H2: `mb-6` (1.5rem / 24px)
  - H3: `mb-4` (1rem / 16px)

#### Paragraphs
- **Margin Bottom**: `mb-10` (2.5rem / 40px) for hero description
- **Margin Top**: `mt-2` (0.5rem / 8px) for secondary text

#### Line Breaks
- **Usage**: `<br />` for multi-line headlines

---

## Layout & Structure

### Z-Index Layers
- **Background Layer**: `z-0` - Dot shader background (fixed)
- **Content Layer**: `z-10` - Main content sections
- **Header Layer**: `z-20` - Logo/header (absolute positioned)

### Positioning

#### Fixed Elements
- **Dot Shader Background**: `fixed inset-0` - Covers entire viewport
- **Pointer Events**: `pointer-events-none` on container, `pointer-events-auto` on canvas

#### Absolute Elements
- **Header**: `absolute top-0 left-0 right-0` - Fixed at top of hero section
- **Logo Glow**: `absolute inset-0` - Behind logo for glow effect

#### Relative Elements
- **Sections**: `relative` - For z-index stacking context
- **Containers**: `relative` - For absolute child positioning

### Flexbox Layouts

#### Hero Section
- **Display**: `flex flex-col`
- **Alignment**: `items-center justify-center`
- **Height**: `h-screen` (100vh)

#### Button Groups
- **Display**: `flex`
- **Direction**: `flex-col sm:flex-row` (column on mobile, row on desktop)
- **Alignment**: `items-center justify-center`
- **Gap**: `gap-4` (1rem / 16px)

#### Header
- **Display**: `flex`
- **Alignment**: `items-center justify-center`
- **Gap**: `gap-3` (0.75rem / 12px)

### Grid Layouts
- Not used on landing page (removed features section)

---

## Visual Effects

### Shadows

#### Card Shadows
- **Standard**: `shadow-2xl` - Large shadow for depth
- **Button Hover**: `hover:shadow-xl` - Enhanced shadow on hover
- **Button Standard**: `shadow-lg` - Medium shadow for buttons

### Blur Effects

#### Backdrop Blur
- **Property**: `backdrop-blur-sm` (4px blur)
- **Usage**: Glassmorphism cards and containers
- **Effect**: Creates frosted glass appearance

#### Logo Glow
- **Blur**: `blur-sm` (4px blur)
- **Opacity**: `opacity-50` (50%)
- **Background**: `bg-white/20`
- **Usage**: Creates subtle glow behind logo

### Border Radius

#### Standard Radius
- **Cards**: `rounded-2xl` (1rem / 16px)
- **Buttons**: `rounded-lg` (0.5rem / 8px)
- **Logo Container**: `rounded-lg` (0.5rem / 8px)
- **Play Button**: `rounded-full` (50% - perfect circle)

### Borders

#### Border Widths
- **Standard**: `border` (1px)
- **Buttons**: `border-2` (2px) for outline buttons

#### Border Styles
- **Color**: Various white opacity levels (see Color Palette)
- **Usage**: Subtle separation and definition

### Transforms

#### Hover Effects
- **Translate Y**: `hover:-translate-y-0.5` (moves up 2px on hover)
- **Scale**: `group-hover:scale-110` (110% scale on hover for icons)
- **Duration**: `transition-all duration-200` (200ms transitions)

---

## Component Styles

### Buttons

#### Primary Button (Get Started)
- **Background**: `bg-white`
- **Text Color**: `text-black`
- **Hover Background**: `hover:bg-gray-200`
- **Padding**: `px-8 py-6`
- **Font Size**: `text-lg` (1.125rem / 18px)
- **Font Weight**: `font-semibold` (600)
- **Border Radius**: `rounded-lg`
- **Shadow**: `shadow-lg hover:shadow-xl`
- **Transform**: `hover:-translate-y-0.5`
- **Transition**: `transition-all duration-200`

#### Secondary Button (See It In Action)
- **Background**: `bg-transparent`
- **Text Color**: `text-white`
- **Border**: `border-2 border-white/50`
- **Hover Border**: `hover:border-white`
- **Hover Background**: `hover:bg-white/10`
- **Padding**: `px-8 py-6`
- **Font Size**: `text-lg`
- **Font Weight**: `font-semibold`
- **Border Radius**: `rounded-lg`
- **Transition**: `transition-all duration-200`
- **Icon**: `flex items-center gap-2`

### Logo Container

#### Outer Container
- **Position**: `relative`
- **Glow Effect**: `absolute inset-0 bg-white/20 rounded-lg blur-sm opacity-50`

#### Inner Container
- **Background**: `bg-white/10`
- **Border**: `border border-white/20`
- **Padding**: `p-3`
- **Border Radius**: `rounded-lg`
- **Position**: `relative` (above glow)

#### Icon
- **Color**: `text-white`
- **Size**: `text-2xl` (1.5rem / 24px)

### Video Container

#### Outer Container
- **Border Radius**: `rounded-2xl`
- **Overflow**: `overflow-hidden`
- **Shadow**: `shadow-2xl`
- **Border**: `border border-white/10`
- **Background**: `bg-black`
- **Margin Bottom**: `mb-12`

#### Video Aspect Ratio
- **Aspect Ratio**: `aspect-video` (16:9)
- **Background**: `bg-black`
- **Display**: `flex items-center justify-center`

#### Play Button
- **Size**: `w-24 h-24` (6rem / 96px)
- **Background**: `bg-white/10`
- **Border**: `border border-white/20`
- **Border Radius**: `rounded-full`
- **Hover**: `hover:bg-white/20`
- **Transition**: `transition-colors`
- **Cursor**: `cursor-pointer`

---

## Responsive Design

### Breakpoints
- **Mobile**: Default (< 640px)
- **Tablet**: `sm:` (≥ 640px)
- **Desktop**: `md:` (≥ 768px)
- **Large Desktop**: `lg:` (≥ 1024px)

### Responsive Typography

#### Hero Headline
- Mobile: `text-5xl` (48px)
- Tablet: `md:text-6xl` (60px)
- Desktop: `lg:text-7xl` (72px)

#### Hero Description
- Mobile: `text-xl` (20px)
- Desktop: `md:text-2xl` (24px)

#### Section Headings
- Mobile: `text-4xl` (36px)
- Desktop: `md:text-5xl` (48px)

### Responsive Spacing

#### Section Overlap
- **Negative Margin**: `-mt-32 md:-mt-48`
  - Mobile: -8rem (-128px)
  - Desktop: -12rem (-192px)
- **Usage**: Video section overlapping hero section

#### Button Layout
- **Mobile**: `flex-col` (stacked vertically)
- **Desktop**: `sm:flex-row` (horizontal row)

### Responsive Containers
- **Max Width**: Containers use responsive max-widths
- **Padding**: Consistent horizontal padding with `px-6`

---

## Animations & Transitions

### Transitions

#### Standard Transitions
- **Property**: `transition-all`
- **Duration**: `duration-200` (200ms)
- **Usage**: Buttons, interactive elements

#### Color Transitions
- **Property**: `transition-colors`
- **Duration**: Default (150ms)
- **Usage**: Hover states, play button

### Transform Animations

#### Hover Lift
- **Transform**: `hover:-translate-y-0.5` (translate up 2px)
- **Usage**: Primary buttons

#### Icon Scale
- **Transform**: `group-hover:scale-110` (scale to 110%)
- **Usage**: Icons within hoverable containers

### Dot Shader Animation
- **Type**: GPU-accelerated shader animation
- **Effect**: Animated dots with mouse trail interaction
- **Performance**: Uses Three.js WebGL rendering

---

## Accessibility

### Text Contrast
- **Primary Text**: White on black (WCAG AAA compliant)
- **Secondary Text**: White/70 on black (WCAG AA compliant)
- **Tertiary Text**: White/50 on black (WCAG AA compliant)

### Interactive Elements
- **Focus States**: Inherited from Button component
- **Hover States**: Clear visual feedback on all interactive elements
- **Disabled States**: `disabled:opacity-70` for disabled buttons

### Semantic HTML
- **Headings**: Proper heading hierarchy (h1, h2, h3)
- **Sections**: Semantic `<section>` elements
- **Buttons**: Proper `<button>` elements with accessible labels

---

## Implementation Notes

### Tailwind CSS Classes
All styles use Tailwind CSS utility classes for consistency and maintainability.

### Custom Components
- **DotScreenShader**: Custom Three.js component for animated background
- **Button**: shadcn/ui button component with custom styling

### Mix Blend Mode
- **Usage**: `mix-blend-exclusion` on text over dot-shader background
- **Purpose**: Ensures text visibility against animated background
- **Browser Support**: Modern browsers (Chrome, Firefox, Safari, Edge)

### Performance Considerations
- **Fixed Background**: Dot shader uses `fixed` positioning for performance
- **GPU Acceleration**: Shader animations use WebGL for smooth performance
- **Lazy Loading**: Consider lazy loading video section for better initial load

---

## Usage Examples

### Creating a New Section
```tsx
<section className="min-h-screen py-20 px-6 bg-black/0 relative z-10">
  <div className="max-w-6xl mx-auto">
    <h3 className="text-4xl md:text-5xl font-light text-white mb-4">
      Section Title
    </h3>
    <p className="text-xl text-white/70 max-w-2xl mx-auto">
      Section description text
    </p>
  </div>
</section>
```

### Creating a Glassmorphism Card
```tsx
<div className="bg-white/5 backdrop-blur-sm rounded-xl p-8 border border-white/10">
  <h4 className="text-2xl font-semibold text-white mb-3">Card Title</h4>
  <p className="text-white/70 leading-relaxed">Card content</p>
</div>
```

### Creating a Primary Button
```tsx
<button className="px-8 py-6 text-lg bg-white text-black hover:bg-gray-200 rounded-lg font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200">
  Button Text
</button>
```

---

## Version History
- **v1.0** - Initial style guide creation
- Based on BuildFlow landing page implementation
- Last updated: Current implementation

---

## Notes
- All color values use Tailwind's opacity modifiers (e.g., `white/70` = 70% opacity)
- Spacing follows Tailwind's default scale (0.25rem increments)
- Typography uses system fonts for optimal performance
- Dark theme is the primary theme (no light theme variant on landing page)

