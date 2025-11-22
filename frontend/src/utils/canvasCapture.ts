import { ReactFlowInstance } from '@xyflow/react';
import { generateThumbnailFromCanvas } from './thumbnail';

/**
 * Capture a thumbnail from the React Flow canvas
 */
export const captureCanvasThumbnail = async (
  reactFlowInstance: ReactFlowInstance | null,
  options?: {
    width?: number;
    height?: number;
    quality?: number;
  }
): Promise<string | null> => {
  if (!reactFlowInstance) {
    return null;
  }

  try {
    // Get the React Flow viewport element
    const reactFlowElement = document.querySelector('.react-flow');
    if (!reactFlowElement) {
      console.warn('React Flow element not found');
      return null;
    }

    // Fit view to show all content
    reactFlowInstance.fitView({ padding: 0.1, duration: 0 });
    
    // Wait a bit for the viewport to update
    await new Promise(resolve => setTimeout(resolve, 100));

    // Generate thumbnail
    const thumbnail = await generateThumbnailFromCanvas(
      reactFlowElement as HTMLElement,
      options
    );

    return thumbnail;
  } catch (error) {
    console.error('Failed to capture canvas thumbnail:', error);
    return null;
  }
};

