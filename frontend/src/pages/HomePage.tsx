import { useNavigate } from 'react-router-dom';
import { DotScreenShader } from '@/components/ui/dot-shader-background';
import { Button } from '@/components/ui/button';
import { 
  ChevronDown,
  Play,
  Github,
  Twitter,
  Linkedin,
  Mail
} from 'lucide-react';
import { FaProjectDiagram } from 'react-icons/fa';

export function HomePage() {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate('/login');
  };

  const scrollToVideo = () => {
    const videoSection = document.getElementById('video-section');
    videoSection?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-black overflow-x-hidden relative">
      {/* Dot Shader Background - Extended to cover entire page */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="w-full h-full">
          <DotScreenShader />
        </div>
      </div>

      {/* Hero Section */}
      <section className="h-screen relative flex flex-col items-center justify-center overflow-hidden z-10">

        {/* Header/Logo */}
        <header className="absolute top-0 left-0 right-0 z-20 px-6 py-6">
          <div className="max-w-7xl mx-auto flex items-center justify-center">
            <div className="flex items-center gap-3">
              <div className="relative">
                <div className="absolute inset-0 bg-white/20 rounded-lg blur-sm opacity-50"></div>
                <div className="relative bg-white/10 border border-white/20 p-3 rounded-lg">
                  <FaProjectDiagram className="text-white text-2xl" />
                </div>
              </div>
              <h1 className="text-2xl font-bold text-white">BuildFlow</h1>
            </div>
          </div>
        </header>

        {/* Main Hero Content */}
        <div className="relative z-10 text-center px-6 max-w-5xl mx-auto">
          <h2 className="text-5xl md:text-6xl lg:text-7xl font-light tracking-tight mb-6 leading-tight">
            <span className="text-white mix-blend-exclusion">Turn Ideas into</span>
            <br />
            <span className="text-white">
              Stunning
            </span>
            <span className="text-white mix-blend-exclusion"> Architecture Diagrams</span>
          </h2>

          <p className="text-xl md:text-2xl font-light text-white mix-blend-exclusion mb-10 max-w-3xl mx-auto leading-relaxed">
            BuildFlow is <span className="text-white font-semibold">Figma + React Flow</span> for architecture diagrams. 
            Create beautiful system designs from your roughest sketches in seconds.
          </p>

          {/* Call-to-Action Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-8">
            <Button
              onClick={handleGetStarted}
              size="lg"
              className="px-8 py-6 text-lg bg-white text-black hover:bg-gray-200 rounded-lg font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
            >
              Get Started
            </Button>
            <Button
              onClick={scrollToVideo}
              variant="outline"
              size="lg"
              className="px-8 py-6 text-lg bg-transparent text-white border-2 border-white/50 hover:border-white hover:bg-white/10 rounded-lg font-semibold flex items-center gap-2 transition-all duration-200"
            >
              See It In Action
              <ChevronDown className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </section>

      {/* Video Demonstration Section */}
      <section id="video-section" className="min-h-screen py-20 px-6 bg-black/0 relative z-10">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h3 className="text-4xl md:text-5xl font-light text-white mb-4">
              See BuildFlow in Action
            </h3>
            <p className="text-xl text-white/70 max-w-2xl mx-auto">
              Watch how easy it is to create beautiful architecture diagrams in minutes
            </p>
          </div>

          {/* Video Container */}
          <div className="relative rounded-2xl overflow-hidden shadow-2xl border border-white/10 bg-black">
            <div className="aspect-video bg-black flex items-center justify-center">
              {/* Placeholder for video - replace with actual video embed */}
              <div className="text-center">
                <div className="w-24 h-24 bg-white/10 border border-white/20 rounded-full flex items-center justify-center mx-auto mb-6 hover:bg-white/20 transition-colors cursor-pointer">
                  <Play className="w-12 h-12 text-white ml-2" fill="white" />
                </div>
                <p className="text-white/70 text-lg">Video demonstration coming soon</p>
                <p className="text-white/50 text-sm mt-2">
                  Replace this placeholder with your video embed (YouTube, Vimeo, etc.)
                </p>
              </div>
              
              {/* Example: Uncomment and use this for YouTube embed */}
              {/* 
              <iframe
                className="w-full h-full"
                src="https://www.youtube.com/embed/YOUR_VIDEO_ID"
                title="BuildFlow Demo"
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              ></iframe>
              */}
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="py-20 px-6 bg-black/0 relative z-10">
        <div className="max-w-4xl mx-auto text-center">
          <h3 className="text-4xl md:text-5xl font-light text-white mb-6">
            Ready to Build Your First Diagram?
          </h3>
          <p className="text-xl text-white/70 mb-10 max-w-2xl mx-auto">
            Join thousands of developers creating beautiful architecture diagrams with BuildFlow
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button
              onClick={handleGetStarted}
              size="lg"
              className="px-10 py-6 text-lg bg-white text-black hover:bg-gray-200 rounded-lg font-semibold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
            >
              Get Started Free
            </Button>
            <Button
              variant="outline"
              size="lg"
              className="px-10 py-6 text-lg bg-transparent text-white border-2 border-white/50 hover:border-white hover:bg-white/10 rounded-lg font-semibold transition-all duration-200"
            >
              View Documentation
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-black/0 text-white py-12 px-6 border-t border-white/10 relative z-10">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            {/* Brand */}
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="bg-white/10 border border-white/20 p-2 rounded-lg">
                  <FaProjectDiagram className="text-white text-xl" />
                </div>
                <h4 className="text-xl font-bold">BuildFlow</h4>
              </div>
              <p className="text-white/70 text-sm">
                Create stunning architecture diagrams with ease.
              </p>
            </div>

            {/* Product */}
            <div>
              <h5 className="font-semibold mb-4">Product</h5>
              <ul className="space-y-2 text-sm text-white/70">
                <li><a href="#" className="hover:text-white transition-colors">Features</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Pricing</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Templates</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Updates</a></li>
              </ul>
            </div>

            {/* Resources */}
            <div>
              <h5 className="font-semibold mb-4">Resources</h5>
              <ul className="space-y-2 text-sm text-white/70">
                <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Guides</a></li>
                <li><a href="#" className="hover:text-white transition-colors">API Reference</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Support</a></li>
              </ul>
            </div>

            {/* Company */}
            <div>
              <h5 className="font-semibold mb-4">Company</h5>
              <ul className="space-y-2 text-sm text-white/70">
                <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
              </ul>
            </div>
          </div>

          {/* Social Links & Copyright */}
          <div className="border-t border-white/10 pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <a href="#" className="text-white/70 hover:text-white transition-colors" aria-label="GitHub">
                <Github className="w-5 h-5" />
              </a>
              <a href="#" className="text-white/70 hover:text-white transition-colors" aria-label="Twitter">
                <Twitter className="w-5 h-5" />
              </a>
              <a href="#" className="text-white/70 hover:text-white transition-colors" aria-label="LinkedIn">
                <Linkedin className="w-5 h-5" />
              </a>
              <a href="#" className="text-white/70 hover:text-white transition-colors" aria-label="Email">
                <Mail className="w-5 h-5" />
              </a>
            </div>
            <p className="text-sm text-white/50">
              © {new Date().getFullYear()} BuildFlow. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
