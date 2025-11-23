import { useEffect, useState } from 'react';
import { supabaseClient, isSupabaseAvailable } from '../lib/supabaseClient';

interface User {
  id: string;
  email?: string;
  displayName?: string;
}

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      if (!isSupabaseAvailable() || !supabaseClient) {
        setIsLoading(false);
        return;
      }

      try {
        const { data, error } = await supabaseClient.auth.getSession();
        
        if (error) {
          console.error('Error fetching session:', error);
          setUser(null);
          setIsLoading(false);
          return;
        }

        if (data.session?.user) {
          const supabaseUser = data.session.user;
          // Try to get display name from user metadata (Google OAuth provides full_name)
          const displayName = 
            supabaseUser.user_metadata?.full_name ||
            supabaseUser.user_metadata?.name ||
            supabaseUser.email?.split('@')[0] ||
            'User';

          setUser({
            id: supabaseUser.id,
            email: supabaseUser.email,
            displayName,
          });
        } else {
          setUser(null);
        }
      } catch (error) {
        console.error('Error in useAuth:', error);
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    fetchUser();

    // Listen for auth state changes
    if (isSupabaseAvailable() && supabaseClient) {
      const { data: { subscription } } = supabaseClient.auth.onAuthStateChange((_event, session) => {
        if (session?.user) {
          const supabaseUser = session.user;
          const displayName = 
            supabaseUser.user_metadata?.full_name ||
            supabaseUser.user_metadata?.name ||
            supabaseUser.email?.split('@')[0] ||
            'User';

          setUser({
            id: supabaseUser.id,
            email: supabaseUser.email,
            displayName,
          });
        } else {
          setUser(null);
        }
        setIsLoading(false);
      });

      return () => {
        subscription.unsubscribe();
      };
    }
  }, []);

  const signOut = async () => {
    if (!isSupabaseAvailable() || !supabaseClient) {
      return;
    }

    try {
      await supabaseClient.auth.signOut();
      setUser(null);
    } catch (error) {
      console.error('Error signing out:', error);
      throw error;
    }
  };

  return { user, isLoading, signOut };
}

