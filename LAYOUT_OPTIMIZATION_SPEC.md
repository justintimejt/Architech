# Layout Optimization Feature Specification

## Overview

This document outlines implementation strategies for adding a "Optimize Layout" button that automatically reorganizes nodes and edges in workflow diagrams to improve readability, spacing, and overall user experience.

## Current Implementation Analysis

### Existing Layout Logic
- **Location**: `frontend/src/hooks/useProject.ts`
- **Current Algorithm**: Hierarchical layout based on topological levels
- **Spacing**: 200px horizontal, 200px vertical
- **Level Calculation**: Uses `calculateNodeLevels()` to determine node hierarchy based on edge connections
- **Limitations**: 
  - Only applies to nodes added without positions
  - Fixed spacing values
  - No user-triggered optimization
  - No consideration for node sizes or edge crossings

### Current Node/Edge Structure
- **Nodes**: Positioned with `{x, y}` coordinates
- **Edges**: Bezier curves with animation
- **Node Types**: 12 different types (web-server, database, worker, etc.)
- **Canvas**: React Flow with zoom, pan, and minimap

## Optimization Goals

1. **Improved Readability**
   - Better spacing between nodes
   - Reduced edge crossings
   - Clear visual hierarchy

2. **User-Friendly Layout**
   - Consistent spacing
   - Logical flow direction
   - Grouped related nodes

3. **Efficiency**
   - Fast computation
   - Smooth animations
   - Preserves user intent where possible

## Implementation Approaches

### 1. Hierarchical Layout (Sugiyama Algorithm)

**Description**: Organizes nodes in layers based on their position in the graph hierarchy.

**Advantages**:
- Clear top-to-bottom flow
- Natural for workflow diagrams
- Already partially implemented
- Good for directed graphs

**Implementation Strategy**:
```typescript
// Enhanced version of existing calculateNodeLevels
function optimizeHierarchicalLayout(
  nodes: Node[], 
  edges: Edge[],
  options: {
    horizontalSpacing: number;  // e.g., 300px
    verticalSpacing: number;       // e.g., 250px
    centerAlignment: boolean;     // Center nodes at each level
    minNodeDistance: number;      // Minimum distance between any two nodes
  }
): Node[]
```

**Features**:
- Calculate topological levels (already exists)
- Group nodes by level
- Center-align nodes at each level
- Adjust spacing based on node count
- Handle disconnected components separately

**Spacing Improvements**:
- **Horizontal**: 300-400px (increased from 200px)
- **Vertical**: 250-300px (increased from 200px)
- **Dynamic**: Adjust based on number of nodes at each level
- **Minimum**: Ensure at least 150px between any two nodes

### 2. Force-Directed Layout (Spring Algorithm)

**Description**: Simulates physical forces between nodes to find optimal positions.

**Advantages**:
- Natural-looking layouts
- Handles complex graphs well
- Automatically spaces nodes
- Good for undirected or mixed graphs

**Implementation Strategy**:
```typescript
// Use a library like d3-force or implement custom physics
function optimizeForceDirectedLayout(
  nodes: Node[],
  edges: Edge[],
  options: {
    iterations: number;           // Number of simulation steps
    strength: number;             // Edge attraction strength
    repulsion: number;            // Node repulsion strength
    centerGravity: number;        // Pull toward center
    minDistance: number;          // Minimum node distance
  }
): Node[]
```

**Libraries**:
- `d3-force` (D3.js force simulation)
- `react-force-graph` (React wrapper)
- Custom implementation using physics simulation

**Features**:
- Iterative refinement
- Animated transitions
- Configurable forces
- Collision detection

### 3. Grid Layout

**Description**: Arranges nodes in a regular grid pattern.

**Advantages**:
- Predictable and organized
- Easy to scan
- Good for small to medium graphs
- Simple implementation

**Implementation Strategy**:
```typescript
function optimizeGridLayout(
  nodes: Node[],
  options: {
    columns: number;              // Auto-calculate or user-specified
    cellWidth: number;            // e.g., 300px
    cellHeight: number;           // e.g., 250px
    startX: number;              // Grid origin
    startY: number;
    sortBy: 'type' | 'name' | 'connections'; // Grouping strategy
  }
): Node[]
```

**Features**:
- Auto-calculate optimal columns
- Group by node type or connection count
- Maintain aspect ratio
- Sort nodes intelligently

### 4. Circular Layout

**Description**: Arranges nodes in a circle or concentric circles.

**Advantages**:
- Compact for small graphs
- Equal importance to all nodes
- Good for hub-and-spoke patterns
- Visually appealing

**Implementation Strategy**:
```typescript
function optimizeCircularLayout(
  nodes: Node[],
  edges: Edge[],
  options: {
    radius: number;               // Circle radius
    centerX: number;              // Center point
    centerY: number;
    sortBy: 'connections' | 'type' | 'name';
  }
): Node[]
```

**Features**:
- Single or multiple concentric circles
- Sort nodes by importance
- Handle disconnected components

### 5. Hybrid Approach (Recommended)

**Description**: Combine multiple algorithms based on graph characteristics.

**Strategy**:
1. Analyze graph structure (connected components, node count, edge density)
2. Choose appropriate algorithm:
   - **Small graphs (< 10 nodes)**: Grid or Circular
   - **Hierarchical workflows**: Enhanced Hierarchical
   - **Complex networks**: Force-Directed
   - **Mixed**: Apply different algorithms to different components

**Implementation**:
```typescript
function optimizeLayout(
  nodes: Node[],
  edges: Edge[],
  algorithm: 'hierarchical' | 'force' | 'grid' | 'circular' | 'auto',
  options?: LayoutOptions
): Node[]
```

## UI Implementation

### Button Placement

**Option 1: Canvas Controls**
- Add to React Flow's `<Controls />` component
- Custom control button
- Always visible

**Option 2: Toolbar/Header**
- Top toolbar with other actions
- More prominent placement
- Can include dropdown for algorithm selection

**Option 3: Context Menu**
- Right-click on canvas
- "Optimize Layout" option
- Less intrusive

**Recommended**: Option 2 (Toolbar) with algorithm selector

### Button Design

```tsx
<button
  onClick={handleOptimizeLayout}
  className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 
             flex items-center gap-2 transition-colors"
  title="Optimize diagram layout for better readability"
>
  <SparklesIcon className="w-5 h-5" />
  Optimize Layout
</button>
```

### Algorithm Selection UI

```tsx
<select
  value={selectedAlgorithm}
  onChange={(e) => setSelectedAlgorithm(e.target.value)}
  className="px-3 py-2 border rounded-lg"
>
  <option value="auto">Auto (Recommended)</option>
  <option value="hierarchical">Hierarchical</option>
  <option value="force">Force-Directed</option>
  <option value="grid">Grid</option>
  <option value="circular">Circular</option>
</select>
```

### Animation

**Smooth Transitions**:
- Animate node positions over 300-500ms
- Use React Flow's built-in animation or CSS transitions
- Show progress indicator during computation

```typescript
// Animate node position changes
function animateNodePositions(
  oldPositions: Map<string, Position>,
  newPositions: Map<string, Position>,
  duration: number = 400
) {
  // Use requestAnimationFrame for smooth animation
  // Update positions incrementally
}
```

## Spacing Improvements

### Current Issues
- Fixed 200px spacing (too small for readability)
- No consideration for node sizes
- No padding around diagram bounds

### Proposed Spacing Rules

1. **Base Spacing**:
   - Horizontal: 300-350px (increased from 200px)
   - Vertical: 250-300px (increased from 200px)

2. **Dynamic Spacing**:
   - Adjust based on node count at each level
   - More nodes = slightly tighter spacing (but never < 200px)
   - Fewer nodes = more generous spacing

3. **Node Size Consideration**:
   - Measure actual node dimensions
   - Ensure spacing accounts for node width/height
   - Minimum: node width + 100px padding

4. **Edge Routing**:
   - Optimize edge paths to reduce crossings
   - Use React Flow's edge routing options
   - Consider edge bundling for dense graphs

5. **Canvas Padding**:
   - Add 50-100px padding around entire diagram
   - Ensure all nodes are visible after optimization
   - Center diagram in viewport

## Edge Optimization

### Current Edge Configuration
- Type: `bezier`
- Animated: `true`
- Style: Dashed, indigo color

### Optimization Strategies

1. **Reduce Edge Crossings**:
   - Reorder nodes at same level to minimize crossings
   - Use edge routing algorithms
   - Consider edge bundling

2. **Edge Routing**:
   - Use React Flow's `smoothstep` for cleaner paths
   - Implement custom routing for complex cases
   - Avoid overlapping with nodes

3. **Edge Labels**:
   - Position labels to avoid overlaps
   - Show labels only when space allows
   - Use tooltips for edge information

## Implementation Plan

### Phase 1: Basic Hierarchical Optimization
1. Create `optimizeLayout` function in `useProject.ts`
2. Enhance existing `calculateNodeLevels` with better spacing
3. Add "Optimize Layout" button to UI
4. Implement smooth position transitions
5. Test with various graph sizes

### Phase 2: Algorithm Selection
1. Implement force-directed layout option
2. Implement grid layout option
3. Add algorithm selector UI
4. Add "auto" mode that chooses best algorithm

### Phase 3: Advanced Features
1. Edge crossing minimization
2. Node grouping/clustering
3. Layout presets (compact, spacious, etc.)
4. Undo/redo for layout changes

### Phase 4: User Preferences
1. Save layout preferences
2. Remember last used algorithm
3. Custom spacing settings
4. Layout templates

## Code Structure

### New Files to Create

```
frontend/src/
├── utils/
│   └── layoutAlgorithms.ts      # All layout algorithms
├── hooks/
│   └── useLayoutOptimization.ts  # Layout optimization hook
└── components/
    └── LayoutOptimizer.tsx       # UI component for optimization
```

### Modified Files

```
frontend/src/
├── hooks/
│   └── useProject.ts            # Add optimizeLayout function
├── components/
│   └── Canvas/
│       └── Canvas.tsx           # Add optimize button
└── contexts/
    └── ProjectContext.tsx       # Expose optimize function
```

## Algorithm Details

### Enhanced Hierarchical Layout

```typescript
interface HierarchicalLayoutOptions {
  horizontalSpacing: number;      // Default: 300
  verticalSpacing: number;        // Default: 250
  minNodeDistance: number;        // Default: 200
  centerAlignment: boolean;        // Default: true
  padding: number;                // Default: 100
}

function optimizeHierarchicalLayout(
  nodes: Node[],
  edges: Edge[],
  options: HierarchicalLayoutOptions
): Node[] {
  // 1. Calculate levels (existing function)
  const levels = calculateNodeLevels(nodes, edges);
  
  // 2. Group nodes by level
  const nodesByLevel = groupNodesByLevel(nodes, levels);
  
  // 3. Calculate optimal spacing
  const spacing = calculateOptimalSpacing(nodesByLevel, options);
  
  // 4. Position nodes
  const positionedNodes = positionNodesByLevel(
    nodes,
    nodesByLevel,
    spacing,
    options
  );
  
  // 5. Center diagram
  return centerDiagram(positionedNodes, options.padding);
}
```

### Force-Directed Layout (Simplified)

```typescript
interface ForceLayoutOptions {
  iterations: number;             // Default: 300
  strength: number;               // Default: 0.5
  repulsion: number;             // Default: 2000
  centerGravity: number;         // Default: 0.1
  minDistance: number;           // Default: 150
}

function optimizeForceDirectedLayout(
  nodes: Node[],
  edges: Edge[],
  options: ForceLayoutOptions
): Node[] {
  // Initialize positions
  let positions = new Map(nodes.map(n => [n.id, n.position]));
  
  // Run simulation
  for (let i = 0; i < options.iterations; i++) {
    positions = simulateForces(positions, edges, options);
  }
  
  // Apply positions to nodes
  return nodes.map(node => ({
    ...node,
    position: positions.get(node.id) || node.position
  }));
}
```

## User Experience Considerations

### 1. Undo/Redo
- Save layout state before optimization
- Allow users to revert changes
- Store in history stack

### 2. Partial Optimization
- Option to optimize only selected nodes
- Preserve manually positioned nodes
- "Lock" nodes to prevent movement

### 3. Progressive Enhancement
- Show optimization progress
- Allow cancellation
- Preview before applying

### 4. Feedback
- Visual feedback during optimization
- Success/error messages
- Show statistics (nodes moved, spacing improved)

## Performance Considerations

### Optimization
- Use Web Workers for heavy computations
- Limit iterations for large graphs
- Cache level calculations
- Debounce rapid clicks

### Large Graphs
- For graphs with > 50 nodes, use simplified algorithms
- Show warning for very large graphs
- Offer "quick optimize" vs "full optimize"

## Testing Scenarios

1. **Empty Graph**: Should handle gracefully
2. **Single Node**: Should center or position appropriately
3. **Two Nodes**: Should space appropriately
4. **Linear Chain**: Should arrange in a line
5. **Tree Structure**: Should show clear hierarchy
6. **Dense Graph**: Should handle many connections
7. **Disconnected Components**: Should handle separately
8. **Mixed Node Types**: Should work with all 12 types

## Future Enhancements

1. **Interactive Layout**: Drag nodes while maintaining constraints
2. **Layout Templates**: Pre-defined layouts for common patterns
3. **Smart Grouping**: Automatically group related nodes
4. **3D Layout**: Optional 3D visualization
5. **Export Layout**: Save/load layout configurations
6. **AI-Powered**: Use ML to learn user preferences

## Dependencies

### Required
- `@xyflow/react` (already installed)
- React hooks (already available)

### Optional (for advanced algorithms)
- `d3-force` - Force-directed layout
- `dagre` - Hierarchical layout (Sugiyama)
- `cola` - Constraint-based layout

## Example Usage

```typescript
// In Canvas component
const { optimizeLayout } = useProjectContext();

const handleOptimizeLayout = useCallback(() => {
  const optimizedNodes = optimizeLayout(
    nodes,
    edges,
    'hierarchical',
    {
      horizontalSpacing: 300,
      verticalSpacing: 250,
      minNodeDistance: 200,
      centerAlignment: true,
      padding: 100
    }
  );
  
  // Update nodes with animation
  animateToNewPositions(optimizedNodes);
}, [nodes, edges, optimizeLayout]);
```

## Conclusion

The layout optimization feature will significantly improve the user experience by:
- Making diagrams more readable
- Reducing visual clutter
- Providing consistent spacing
- Supporting various graph structures
- Maintaining user control and flexibility

The recommended approach is to start with an enhanced hierarchical layout (building on existing code) and gradually add more algorithms based on user feedback and needs.

