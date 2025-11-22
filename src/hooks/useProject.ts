import { useState, useCallback } from 'react';
import { Node, Edge, Project } from '../types';
import { v4 as uuidv4 } from 'uuid';
import { PROJECT_VERSION } from '../utils/constants';
import { getDefaultNodeName } from '../nodes/nodeConfig';

export const useProject = () => {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  const addNode = useCallback((type: string, position: { x: number; y: number }) => {
    const newNode: Node = {
      id: uuidv4(),
      type,
      position,
      data: {
        name: getDefaultNodeName(type),
        description: '',
        attributes: {}
      }
    };
    setNodes(prev => [...prev, newNode]);
    return newNode.id;
  }, []);

  const updateNode = useCallback((nodeId: string, updates: Partial<Node['data']>) => {
    setNodes(prev =>
      prev.map(node =>
        node.id === nodeId
          ? { ...node, data: { ...node.data, ...updates } }
          : node
      )
    );
  }, []);

  const updateNodePosition = useCallback((nodeId: string, position: { x: number; y: number }) => {
    setNodes(prev =>
      prev.map(node =>
        node.id === nodeId
          ? { ...node, position }
          : node
      )
    );
  }, []);

  const deleteNode = useCallback((nodeId: string) => {
    setNodes(prev => prev.filter(node => node.id !== nodeId));
    setEdges(prev => prev.filter(edge => edge.source !== nodeId && edge.target !== nodeId));
    if (selectedNodeId === nodeId) {
      setSelectedNodeId(null);
    }
  }, [selectedNodeId]);

  const addEdge = useCallback((source: string, target: string) => {
    setEdges(prev => {
      // Check if edge already exists
      const exists = prev.some(
        e => (e.source === source && e.target === target) ||
             (e.source === target && e.target === source)
      );
      if (exists) return prev;

      const newEdge: Edge = {
        id: uuidv4(),
        source,
        target,
        type: 'smoothstep'
      };
      return [...prev, newEdge];
    });
  }, []);

  const deleteEdge = useCallback((edgeId: string) => {
    setEdges(prev => prev.filter(edge => edge.id !== edgeId));
  }, []);

  const loadProject = useCallback((project: Project) => {
    setNodes(project.nodes || []);
    setEdges(project.edges || []);
    setSelectedNodeId(null);
  }, []);

  const getProject = useCallback((): Project => {
    return {
      version: PROJECT_VERSION,
      nodes,
      edges,
      updatedAt: new Date().toISOString()
    };
  }, [nodes, edges]);

  const clearProject = useCallback(() => {
    setNodes([]);
    setEdges([]);
    setSelectedNodeId(null);
  }, []);

  return {
    nodes,
    edges,
    selectedNodeId,
    setSelectedNodeId,
    addNode,
    updateNode,
    updateNodePosition,
    deleteNode,
    addEdge,
    deleteEdge,
    loadProject,
    getProject,
    clearProject
  };
};

