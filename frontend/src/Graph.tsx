import { useEffect, useRef } from "react";
import cytoscape from "cytoscape";
import type { GraphData } from "./types";
const colors: Record<string, string> = {
  Low: "#93c5b7",
  Medium: "#6fa5bf",
  Elevated: "#e7b557",
  High: "#e98255",
  Critical: "#d55361",
  Unknown: "#bcc9ce",
};
export type GraphProps = {
  data: GraphData | null;
  onNode: (id: string) => void;
  onEdge: (id: string) => void;
};
export function Graph({ data, onNode, onEdge }: GraphProps) {
  const container = useRef<HTMLDivElement>(null);
  const callbacks = useRef({ onNode, onEdge });
  callbacks.current = { onNode, onEdge };
  useEffect(() => {
    if (!container.current || !data) return;
    const cy = cytoscape({
      container: container.current,
      elements: [
        ...data.nodes.map((n, i) => ({
          data: { ...n, color: colors[n.severity] ?? colors.Unknown },
          position: { x: (i % 15) * 100, y: Math.floor(i / 15) * 100 },
        })),
        ...data.edges.map((e) => ({ data: e })),
      ],
      style: [
        {
          selector: "node",
          style: {
            "background-color": "data(color)",
            label: "data(label)",
            "font-size": 9,
            color: "#526575",
            "text-valign": "bottom",
            "text-margin-y": 7,
            width: 24,
            height: 24,
            "border-width": 2,
            "border-color": "#fff",
          },
        },
        {
          selector: "node[?blacklisted]",
          style: { "border-color": "#aa2843", "border-width": 4 },
        },
        {
          selector: "edge",
          style: {
            width: 1.2,
            "line-color": "#c5d7db",
            "target-arrow-color": "#b4cbd0",
            "target-arrow-shape": "triangle",
            "curve-style": "bezier",
            "arrow-scale": 0.7,
          },
        },
        {
          selector: ":selected",
          style: {
            "background-color": "#136c70",
            "line-color": "#136c70",
            "target-arrow-color": "#136c70",
            "border-width": 4,
            "border-color": "#f0b663",
          },
        },
      ],
      layout: {
        name: "cose",
        animate: false,
        randomize: false,
        nodeRepulsion: () => 8500,
        idealEdgeLength: () => 65,
        fit: true,
        padding: 40,
      } as cytoscape.CoseLayoutOptions,
      minZoom: 0.08,
      maxZoom: 4,
      wheelSensitivity: 0.2,
    });
    cy.on("tap", "node", (event) =>
      callbacks.current.onNode(event.target.id()),
    );
    cy.on("tap", "edge", (event) =>
      callbacks.current.onEdge(event.target.id()),
    );
    const resize = new ResizeObserver(() => cy.resize());
    resize.observe(container.current);
    return () => {
      resize.disconnect();
      cy.destroy();
    };
  }, [data]);
  return (
    <div
      className="graph-canvas"
      ref={container}
      role="img"
      aria-label="Đồ thị dòng tiền. Dùng bảng giao dịch và bằng chứng để truy cập bằng bàn phím."
    />
  );
}
