export default function Skeleton({ h = 12, w = "100%", r = 8, style }) {
  return (
    <div style={{
      height: h, width: w, borderRadius: r, background:
      "linear-gradient(90deg,#f4f4f4 25%, #ececec 37%, #f4f4f4 63%)",
      backgroundSize: "400% 100%", animation: "shimmer 1.3s infinite", ...style
    }}/>
  );
}
