import { createContext, useContext, useState, ReactNode } from 'react';
import { ReactFlowInstance } from '@xyflow/react';

interface ReactFlowContextType {
  reactFlowInstance: ReactFlowInstance | null;
  setReactFlowInstance: (instance: ReactFlowInstance | null) => void;
}

const ReactFlowContext = createContext<ReactFlowContextType | undefined>(undefined);

export function ReactFlowProvider({ children }: { children: ReactNode }) {
  const [reactFlowInstance, setReactFlowInstance] = useState<ReactFlowInstance | null>(null);

  return (
    <ReactFlowContext.Provider value={{ reactFlowInstance, setReactFlowInstance }}>
      {children}
    </ReactFlowContext.Provider>
  );
}

export function useReactFlowContext() {
  const context = useContext(ReactFlowContext);
  if (context === undefined) {
    throw new Error('useReactFlowContext must be used within a ReactFlowProvider');
  }
  return context;
}

