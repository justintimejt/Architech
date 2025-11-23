// frontend/src/pages/LoginPage.tsx
import { useNavigate } from 'react-router-dom';
import { LoginCard } from '../components/auth';
import { DotScreenShader } from '@/components/ui/dot-shader-background';
import { ArrowLeft } from 'lucide-react';

export function LoginPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-black overflow-x-hidden relative">
      {/* Dot Shader Background - Extended to cover entire page */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="w-full h-full">
          <DotScreenShader />
        </div>
      </div>

      {/* Header */}
      <header className="absolute top-0 left-0 right-0 z-20 px-6 py-6">
        <div className="max-w-7xl mx-auto">
          {/* Back Arrow Button */}
          <button
            onClick={() => navigate('/')}
            className="flex items-center gap-2 text-white hover:text-white/80 transition-colors"
            aria-label="Go back to home"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
        </div>
      </header>

      {/* Login Card */}
      <div className="relative z-10 min-h-screen flex items-center justify-center px-6 py-20">
        <LoginCard />
      </div>
    </div>
  );
}

