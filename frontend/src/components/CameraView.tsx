import { useCallback, useEffect, useRef, useState } from 'react';
import { Box, Button, CircularProgress, Stack, Typography } from '@mui/material';

import { PipelineFace, runPipeline } from '../api/client';
import EmotionBar from './EmotionBar';
import LatencyBadge from './LatencyBadge';
import Overlay from './Overlay';

interface CameraViewProps {
  intervalMs?: number;
  topK: number;
  threshold: number;
}

export default function CameraView({ intervalMs = 250, topK, threshold }: CameraViewProps) {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const [faces, setFaces] = useState<PipelineFace[]>([]);
  const [running, setRunning] = useState(false);
  const [latency, setLatency] = useState<number>();
  const [error, setError] = useState<string | null>(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

  const captureFrame = useCallback(async () => {
    const video = videoRef.current;
    if (!video) return;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const blob = await new Promise<Blob | null>((resolve) => canvas.toBlob(resolve, 'image/jpeg', 0.85));
    if (!blob) return;
    const reader = new FileReader();
    const base64 = await new Promise<string>((resolve) => {
      reader.onloadend = () => resolve(reader.result as string);
      reader.readAsDataURL(blob);
    });
    const start = performance.now();
    try {
      const result = await runPipeline({ imageBase64: base64, topK, threshold });
      setFaces(result.faces);
      setLatency(result.timing_ms.total ?? performance.now() - start);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to run pipeline');
    }
  }, [topK, threshold]);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    let stream: MediaStream;
    const start = async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } });
        video.srcObject = stream;
        await video.play();
        setDimensions({ width: video.videoWidth, height: video.videoHeight });
        setRunning(true);
      } catch (err) {
        setError('Unable to access camera.');
      }
    };
    start();
    return () => {
      stream?.getTracks().forEach((track) => track.stop());
      setRunning(false);
    };
  }, []);

  useEffect(() => {
    const handler = () => {
      const video = videoRef.current;
      if (video) {
        setDimensions({ width: video.videoWidth, height: video.videoHeight });
      }
    };
    const video = videoRef.current;
    video?.addEventListener('loadedmetadata', handler);
    return () => video?.removeEventListener('loadedmetadata', handler);
  }, []);

  useEffect(() => {
    if (!running) return;
    const timer = setInterval(() => {
      void captureFrame();
    }, intervalMs);
    return () => clearInterval(timer);
  }, [running, captureFrame, intervalMs]);

  return (
    <Stack spacing={2} alignItems="center">
      <Box position="relative" sx={{ width: 'min(640px, 100%)' }}>
        <video ref={videoRef} playsInline muted style={{ width: '100%', borderRadius: 12 }} />
        <Overlay faces={faces} width={dimensions.width} height={dimensions.height} />
      </Box>
      <Stack direction="row" spacing={2} alignItems="center">
        <LatencyBadge latency={latency} />
        {!running && <CircularProgress size={20} />}
      </Stack>
      {error && (
        <Typography color="error" variant="body2">
          {error}
        </Typography>
      )}
      <Stack direction="row" spacing={2}>
        {faces.map((face, idx) => (
          <EmotionBar key={idx} probabilities={face.emotion?.probabilities || {}} />
        ))}
      </Stack>
      <Button variant="outlined" onClick={() => void captureFrame()}>
        Capture Now
      </Button>
    </Stack>
  );
}
