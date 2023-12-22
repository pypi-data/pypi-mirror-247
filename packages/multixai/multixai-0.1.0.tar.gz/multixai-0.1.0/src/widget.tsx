import ReactDOM from "react-dom/client";
import './index.css'
import App from './App.tsx'

// the render function is for the anywidget
export function render({ model, el }) {
    const root = ReactDOM.createRoot(el);
    root.render(<App exp={model.get("exp")} />);
    return () => root.unmount();
  }