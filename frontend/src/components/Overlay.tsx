import { useEffect, useRef } from 'react';

import { PipelineFace } from '../api/client';

interface OverlayProps {
  faces: PipelineFace[];
  width: number;
  height: number;
}

export default function Overlay({ faces, width, height }: OverlayProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.clearRect(0, 0, width, height);
    ctx.lineWidth = 2;
    ctx.font = '14px Inter';
    faces.forEach((face) => {
      const [x, y, w, h] = face.bbox;
      ctx.strokeStyle = '#38bdf8';
      ctx.strokeRect(x, y, w, h);
      const label = face.identity?.person ?? 'Unknown';
      const emotion = face.emotion?.label ? ` • ${face.emotion?.label}` : '';
      ctx.fillStyle = 'rgba(15, 23, 42, 0.7)';
      ctx.fillRect(x, Math.max(y - 20, 0), ctx.measureText(label + emotion).width + 12, 20);
      ctx.fillStyle = '#f8fafc';
      ctx.fillText(`${label}${emotion}`, x + 6, Math.max(y - 6, 12));
    });
  }, [faces, width, height]);

  return <canvas ref={canvasRef} style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }} />;
}
