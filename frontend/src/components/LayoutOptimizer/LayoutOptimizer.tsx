import { useState, useCallback } from 'react';
import { useReactFlow } from '@xyflow/react';
import { useProjectContext } from '../../contexts/ProjectContext';
import { optimizeLayout as calculateLayout } from '../../utils/layoutAlgorithms';
import { FaMagic, FaSpinner } from 'react-icons/fa';
import type { LayoutAlgorithm } from '../../utils/layoutAlgorithms';

interface LayoutOptimizerProps {
  className?: string;
}

export function LayoutOptimizer({ className = '' }: LayoutOptimizerProps) {
  const { nodes, edges, updateNodePosition } = useProjectContext();
  const { setNodes, fitView } = useReactFlow();
  const [selectedAlgorithm, setSelectedAlgorithm] = useState<LayoutAlgorithm>('auto');
  const [isOptimizing, setIsOptimizing] = useState(false);

  const handleOptimize = useCallback(async () => {
    if (nodes.length === 0) {
      return;
    }

    setIsOptimizing(true);

    try {
      // Save current positions for animation
      const oldPositions = new Map(nodes.map(n => [n.id, { ...n.position }]));

      // Calculate optimized positions (without updating state yet)
      const optimizedNodes = calculateLayout(nodes, edges, selectedAlgorithm);
      const newPositions = new Map(optimizedNodes.map(n => [n.id, { ...n.position }]));

      // Animate to new positions using ReactFlow's setNodes
      await animateNodePositions(oldPositions, newPositions, 400);

      // After animation completes, update the project context with final positions
      // This ensures the positions are persisted to the project state
      optimizedNodes.forEach(node => {
        updateNodePosition(node.id, node.position);
      });

      // Fit view to show all nodes
      setTimeout(() => {
        fitView({ padding: 0.1, duration: 300 });
      }, 100);
    } catch (error) {
      console.error('Error optimizing layout:', error);
    } finally {
      setIsOptimizing(false);
    }
  }, [nodes, edges, selectedAlgorithm, updateNodePosition, setNodes, fitView]);

  // Animate node positions smoothly
  const animateNodePositions = useCallback((
    oldPositions: Map<string, { x: number; y: number }>,
    newPositions: Map<string, { x: number; y: number }>,
    duration: number = 400
  ): Promise<void> => {
    return new Promise((resolve) => {
      const startTime = Date.now();

      const animate = () => {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function (ease-out)
        const eased = 1 - Math.pow(1 - progress, 3);

        setNodes((nds) =>
          nds.map((n) => {
            const oldPos = oldPositions.get(n.id);
            const newPos = newPositions.get(n.id);
            
            if (oldPos && newPos) {
              const currentX = oldPos.x + (newPos.x - oldPos.x) * eased;
              const currentY = oldPos.y + (newPos.y - oldPos.y) * eased;
              
              return { ...n, position: { x: currentX, y: currentY } };
            }
            return n;
          })
        );

        if (progress < 1) {
          requestAnimationFrame(animate);
        } else {
          // Final update to ensure exact positions
          setNodes((nds) =>
            nds.map((n) => {
              const newPos = newPositions.get(n.id);
              return newPos ? { ...n, position: newPos } : n;
            })
          );
          resolve();
        }
      };

      requestAnimationFrame(animate);
    });
  }, [setNodes]);

  const isDisabled = nodes.length === 0 || isOptimizing;

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <select
        value={selectedAlgorithm}
        onChange={(e) => setSelectedAlgorithm(e.target.value as LayoutAlgorithm)}
        disabled={isDisabled}
        className="px-3 py-1.5 text-sm border border-gray-300 rounded-lg bg-white 
                   disabled:bg-gray-100 disabled:text-gray-400 disabled:cursor-not-allowed
                   focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
        title="Select layout algorithm"
      >
        <option value="auto">Auto (Recommended)</option>
        <option value="hierarchical">Hierarchical</option>
        <option value="force">Force-Directed</option>
        <option value="grid">Grid</option>
        <option value="circular">Circular</option>
      </select>
      
      <button
        onClick={handleOptimize}
        disabled={isDisabled}
        className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 
                   disabled:bg-gray-400 disabled:cursor-not-allowed
                   flex items-center gap-2 transition-colors duration-200
                   focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        title="Optimize diagram layout for better readability"
      >
        {isOptimizing ? (
          <>
            <FaSpinner className="w-4 h-4 animate-spin" />
            <span className="text-sm">Optimizing...</span>
          </>
        ) : (
          <>
            <FaMagic className="w-4 h-4" />
            <span className="text-sm">Optimize Layout</span>
          </>
        )}
      </button>
    </div>
  );
}

