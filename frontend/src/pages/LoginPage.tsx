// frontend/src/pages/LoginPage.tsx
import { LoginCard } from '../components/auth';
import { DotScreenShader } from '@/components/ui/dot-shader-background';
import { FaProjectDiagram } from 'react-icons/fa';

export function LoginPage() {
  return (
    <div className="min-h-screen bg-black overflow-x-hidden relative">
      {/* Dot Shader Background - Extended to cover entire page */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="w-full h-full">
          <DotScreenShader />
        </div>
      </div>

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

      {/* Login Card */}
      <div className="relative z-10 min-h-screen flex items-center justify-center px-6 py-20">
        <LoginCard />
      </div>
    </div>
  );
}

