# Visual System Design Editor

A lightweight, browser-based visual editor for designing system architectures through an intuitive drag-and-drop interface.

## Features

- 🎨 **Interactive Canvas** - Zoomable and pannable drawing surface
- 📦 **Component Library** - 12 predefined system component types
- 🔗 **Connection System** - Draw edges between nodes
- ✏️ **Node Configuration** - Edit metadata through inspector panel
- 💾 **Persistence** - Save/load projects locally (localStorage + JSON)
- 📤 **Export** - Export diagrams as PNG images

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser and navigate to `http://localhost:5173`

### Build for Production

```bash
npm run build
```

The production build will be in the `dist` directory.

## Usage

### Creating a Diagram

1. **Add Components**: Drag components from the left sidebar onto the canvas
2. **Connect Nodes**: Click and drag from a node's connection handle to another node
3. **Edit Properties**: Click on a node to open the inspector panel on the right
4. **Save Project**: Click "Save" in the toolbar to save to localStorage
5. **Export**: Click "Export PNG" to download your diagram as an image

### Component Types

- Web Server
- Database
- Worker
- Cache
- Queue
- Storage
- Third-party API
- Compute Node
- Load Balancer
- Message Broker
- CDN
- Monitoring Service

## Project Structure

```
src/
├── components/
│   ├── Canvas/          # Main canvas component
│   ├── SidebarLeft/     # Component library
│   ├── SidebarRight/    # Inspector panel
│   └── Toolbar/         # Top toolbar
├── contexts/            # React contexts
├── hooks/               # Custom hooks
├── nodes/               # Node type definitions
├── types/               # TypeScript type definitions
├── utils/               # Utility functions
└── styles/              # Global styles
```

## Technology Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **React Flow** - Diagram engine
- **TailwindCSS** - Styling
- **html2canvas** - PNG export

## License

MIT

