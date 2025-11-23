# React AI Chatbot Interface
URL: /blocks/ai-chatbot
React AI chatbot with streaming responses and reasoning display. Complete ChatGPT-style interface with model selection, sources, and TypeScript support using shadcn/ui.

***

title: React AI Chatbot Interface
description: React AI chatbot with streaming responses and reasoning display. Complete ChatGPT-style interface with model selection, sources, and TypeScript support using shadcn/ui.
icon: MessageCircle
-------------------

<PoweredBy
  packages={[
  { name: "React", url: "https://react.dev" },
  { name: "AI Conversation", url: "/components/ai-conversation" },
  { name: "AI Message", url: "/components/ai-message" },
  { name: "AI Prompt Input", url: "/components/ai-prompt-input" },
  { name: "AI Reasoning", url: "/components/ai-reasoning" },
  { name: "AI Sources", url: "/components/ai-sources" },
  { name: "Lucide React", url: "https://lucide.dev/" },
  { name: "Tailwind CSS", url: "https://tailwindcss.com" },
]}
/>

<Callout title="Building AI chat interfaces?">
  [Join our Discord community](https://discord.com/invite/Z9NVtNE7bj) for help
  from other developers.
</Callout>

<br />

Everyone's building AI chat now. Slap together a text input and div for messages, call it done. Then spend three weeks debugging why messages flicker during streaming, scroll jumps around, and users can't tell when the AI is thinking versus broken. This React component handles the annoying stuff—proper streaming states, scroll management, and all the UI details users expect from ChatGPT.

<Preview path="ai-chatbot" type="block" />

Built with TypeScript and shadcn/ui. Combines dedicated AI components for conversation display, message formatting, prompt input, and reasoning sections. The component handles streaming coordination, scroll management, and state updates so you can focus on connecting your AI API.

## Why most AI chat UIs suck

Your basic chat implementation works fine until users start actually using it. Messages arrive character by character but the scroll jumps around. No visual feedback when the AI is thinking—users assume it's broken. The model dropdown conflicts with the input focus. Auto-scroll fights with manual scrolling. Trust me, I've debugged this exact combination at least five times.

This component handles the coordination nightmares: streaming without scroll jumping, typing indicators that don't break layout, model switching that doesn't lose focus, and proper loading states throughout. Plus reasoning sections and source citations because users expect transparency now, not just raw responses.

Built with accessibility in mind—screen readers work with streaming content, keyboard navigation doesn't break during updates, and touch targets are sized properly for mobile.

## Installation

<Installer packageName="ai-chatbot" />

## Usage

```tsx
import {
  Conversation,
  ConversationContent,
  ConversationScrollButton,
} from '@repo/ai/conversation';
import { Message, MessageAvatar, MessageContent } from '@repo/ai/message';
import {
  PromptInput,
  PromptInputSubmit,
  PromptInputTextarea,
  PromptInputToolbar,
} from '@repo/ai/prompt-input';
import { Reasoning, ReasoningContent, ReasoningTrigger } from '@repo/ai/reasoning';
import { Sources, SourcesContent, SourcesTrigger } from '@repo/ai/sources';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);

  return (
    <div className="flex h-full w-full flex-col">
      <Conversation className="flex-1">
        <ConversationContent>
          {messages.map((message) => (
            <Message key={message.id} from={message.role}>
              <MessageContent>{message.content}</MessageContent>
              <MessageAvatar src={message.avatar} name={message.name} />
            </Message>
          ))}
        </ConversationContent>
        <ConversationScrollButton />
      </Conversation>
      
      <PromptInput onSubmit={handleSubmit}>
        <PromptInputTextarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me anything..."
        />
        <PromptInputToolbar>
          <PromptInputSubmit disabled={!input.trim()} />
        </PromptInputToolbar>
      </PromptInput>
    </div>
  );
};
```

## Features

* **Streaming that doesn't break scroll** - Messages appear character by character without jumping the viewport around
* **Smart auto-scroll management** - Stays at bottom during streaming, lets users read history without fighting back
* **Model switching** - Dropdown for GPT-4, Claude, Gemini, etc. with persistence and proper state coordination
* **Reasoning sections** - Collapsible "thinking" display that auto-expands during AI reasoning, manual toggle after
* **Source citations** - Expandable reference links with automatic counting ("Used 3 sources")
* **Proper loading states** - Typing indicators, submit button states, and visual feedback throughout
* **TypeScript everywhere** - Complete interfaces for messages, reasoning, sources, and streaming states
* **Touch-friendly mobile** - 44px touch targets, virtual keyboard handling, responsive conversation layout
* **Keyboard shortcuts** - Enter to send, Shift+Enter for newlines, Escape to cancel, Tab navigation
* **Copy-paste ready** - Import the components, connect your API, done. No state management confusion
* **shadcn/ui integration** - Uses existing design tokens and works with your theme customization
* **Screen reader friendly** - ARIA live regions for streaming, proper focus management, reduced motion support

## Use Cases

This free open source React component works perfectly for:

* **AI customer support** - Interactive help systems with reasoning transparency and source attribution in Next.js applications
* **Development assistants** - Code help chatbots with model selection and conversation management using TypeScript
* **Content creation tools** - Writing assistants with streaming responses and multi-model support
* **Educational platforms** - Learning chatbots with step-by-step reasoning display and source verification
* **Research interfaces** - AI research tools with citation tracking and conversation organization
* **Documentation helpers** - Interactive docs with AI guidance and contextual source linking
* **Product demos** - Showcase AI capabilities with professional chat interfaces and model comparison
* **Enterprise applications** - Internal AI tools with audit trails and reasoning transparency

## API Reference

### AIChatbot

The main chatbot interface component providing complete conversational AI functionality.

| Prop            | Type                        | Default | Description                                  |
| --------------- | --------------------------- | ------- | -------------------------------------------- |
| `messages`      | `ChatMessage[]`             | `[]`    | Array of conversation messages with metadata |
| `onMessageSend` | `(message: string) => void` | -       | Callback when user sends a message           |
| `isStreaming`   | `boolean`                   | `false` | Whether AI is currently responding           |
| `selectedModel` | `string`                    | -       | Currently selected AI model identifier       |
| `onModelChange` | `(model: string) => void`   | -       | Callback when user changes AI model          |
| `className`     | `string`                    | -       | Additional CSS classes for container         |
| `...props`      | `HTMLAttributes`            | -       | All HTML div attributes supported            |

### ChatMessage Interface

| Property      | Type                    | Description                           |
| ------------- | ----------------------- | ------------------------------------- |
| `id`          | `string`                | Unique message identifier             |
| `content`     | `string`                | Message text content                  |
| `role`        | `'user' \| 'assistant'` | Message sender role                   |
| `timestamp`   | `Date`                  | Message creation time                 |
| `reasoning`   | `string`                | Optional AI reasoning text            |
| `sources`     | `Source[]`              | Optional citation sources             |
| `isStreaming` | `boolean`               | Whether message is actively streaming |

### Conversation Management

The component automatically handles:

* **Message state** with proper React state updates and re-rendering
* **Scroll behavior** with auto-scroll to latest and manual scroll controls
* **Streaming coordination** between input states and message display
* **Model persistence** saving user preferences to localStorage

### Streaming Specifications

| Element           | Behavior                       | Animation       | Accessibility          |
| ----------------- | ------------------------------ | --------------- | ---------------------- |
| Message content   | Character-by-character display | 50ms intervals  | Screen reader friendly |
| Reasoning section | Auto-expand when complete      | Slide animation | Keyboard navigable     |
| Sources list      | Appear after message           | Fade in         | Focus management       |
| Typing indicator  | Pulsing loader                 | Continuous      | ARIA live region       |

## Common gotchas

**Message streaming performance**: Character-by-character updates can cause React re-render performance issues with long messages. The component uses optimized state updates and memoization to handle this efficiently.

**Conversation scroll management**: Auto-scrolling during streaming can conflict with user manual scrolling. The component detects user scroll intent and temporarily disables auto-scroll until the user returns to bottom.

**Model switching during streaming**: Changing models while a message is streaming can cause state conflicts. The component properly cancels ongoing streams and resets state when model selection changes.

**Accessibility with dynamic content**: Screen readers struggle with rapidly changing content during streaming. The component uses ARIA live regions and proper focus management to ensure accessibility.

**Mobile keyboard interactions**: Virtual keyboards on mobile can disrupt conversation scrolling and input focus. The component handles viewport changes and maintains proper scroll positioning.

**TypeScript message types**: Strict typing for AI messages requires proper interface definitions. Ensure your message objects match the ChatMessage interface for full type safety.

## Explore the components it's built with

This AI chatbot combines multiple specialized AI components from our collection:

<Cards>
  <Card href="/ai/conversation" title="Conversation" description="Scrollable conversation container with auto-scroll and manual controls" />

  <Card href="/ai/message" title="Message" description="Individual message display with avatars and content formatting" />

  <Card href="/ai/prompt-input" title="Prompt Input" description="Advanced input component with model selection and tool buttons" />

  <Card href="/ai/reasoning" title="Reasoning" description="Collapsible reasoning display showing AI thought processes" />

  <Card href="/ai/sources" title="Sources" description="Expandable source citations for AI response transparency" />

  <Card href="/ai/loader" title="Loader" description="Animated loading indicator for AI processing states" />
</Cards>

## Questions developers actually ask

<Accordions type="single">
  <Accordion id="openai-integration" title="How do I connect this to OpenAI or Anthropic APIs?">
    This handles the UI, you handle the API. Use Vercel AI SDK or just fetch() with streaming. Update the messages state as responses come in. The component accepts any object matching the ChatMessage interface—doesn't care where the data comes from.
  </Accordion>

  <Accordion id="scroll-jumping" title="Why does my scroll position jump around during streaming?">
    Classic problem. The component tracks whether users are manually scrolling and only auto-scrolls when they're at the bottom. Uses proper scroll restoration and doesn't fight with user intent. Way better than naive "always scroll to bottom" approaches.
  </Accordion>

  <Accordion id="model-switching" title="Can I add more AI models to the dropdown?">
    Yeah, just pass your models array. Works with any provider—OpenAI, Anthropic, local models, whatever. The component persists the selection and handles switching without breaking ongoing streams.
  </Accordion>

  <Accordion id="streaming-performance" title="Does character-by-character streaming cause performance issues?">
    It can if you're naive about it. The component uses optimized React updates and proper memoization. Won't cause re-render storms like basic implementations do. Tested with 2000+ character responses.
  </Accordion>

  <Accordion id="mobile-keyboard" title="How does this handle mobile virtual keyboards?">
    Virtual keyboards are annoying—they resize the viewport and mess up scroll positioning. The component detects these changes and maintains proper scroll state. Input stays focused, conversation stays readable.
  </Accordion>

  <Accordion id="conversation-persistence" title="How do I save conversations across browser sessions?">
    Messages live in React state. For persistence, JSON.stringify the messages array to localStorage, send to your backend, whatever. Restore on mount. The component doesn't care about your storage strategy.
  </Accordion>

  <Accordion id="reasoning-timing" title="When do the reasoning sections appear?">
    Include a reasoning property in your message objects. The sections auto-expand during streaming (so users see the AI "thinking"), then become manually toggleable. Same pattern ChatGPT uses.
  </Accordion>

  <Accordion id="bundle-size" title="What's the bundle impact of all these AI components?">
    The whole AI component collection is \~15kb gzipped. Individual components are smaller—Conversation (\~3kb), Message (\~2kb), PromptInput (\~4kb). Tree-shaking works properly so you only bundle what you import.
  </Accordion>
</Accordions>
