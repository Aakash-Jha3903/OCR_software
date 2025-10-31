export default function Spinner({ size = 18 }) {
  const s = {
    width: size, height: size, borderRadius: "50%",
    border: "2px solid #ddd", borderTopColor: "#111",
    animation: "spin 0.9s linear infinite", display:"inline-block"
  };
  return (
    <>
      <span style={s} />
      <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
    </>
  );
}
