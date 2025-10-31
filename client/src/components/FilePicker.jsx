// src/components/FilePicker.jsx
export default function FilePicker({ label = "Select image", onChange }) {
  return (
    <div>
      <div className="label">{label}</div>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => onChange?.(e.target.files?.[0] || null)}
      />
    </div>
  );
}
