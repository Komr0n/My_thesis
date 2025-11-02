import { ChangeEvent, useRef, useState } from 'react';
import { Box, Button, Card, CardContent, Stack, Typography } from '@mui/material';

import { PipelineFace, uploadPipeline } from '../api/client';
import EmotionBar from './EmotionBar';
import Overlay from './Overlay';

interface PhotoUploadProps {
  onLatency?: (latency: number) => void;
}

export default function PhotoUpload({ onLatency }: PhotoUploadProps) {
  const [faces, setFaces] = useState<PipelineFace[]>([]);
  const [imageUrl, setImageUrl] = useState<string>();
  const [error, setError] = useState<string | null>(null);
  const imgRef = useRef<HTMLImageElement | null>(null);

  const onChange = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    const preview = URL.createObjectURL(file);
    setImageUrl(preview);
    const formData = new FormData();
    formData.append('file', file);
    const start = performance.now();
    try {
      const response = await uploadPipeline(formData);
      setFaces(response.faces);
      onLatency?.(response.timing_ms.total ?? performance.now() - start);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to process photo');
    }
  };

  return (
    <Stack spacing={2} alignItems="center">
      <Button variant="contained" component="label">
        Upload Photo
        <input type="file" accept="image/*" hidden onChange={onChange} />
      </Button>
      {error && <Typography color="error">{error}</Typography>}
      {imageUrl && (
        <Card sx={{ width: 'min(640px, 100%)' }}>
          <CardContent>
            <Box position="relative">
              <img ref={imgRef} src={imageUrl} alt="preview" style={{ width: '100%', borderRadius: 12 }} />
              <Overlay
                faces={faces}
                width={imgRef.current?.naturalWidth || 640}
                height={imgRef.current?.naturalHeight || 360}
              />
            </Box>
          </CardContent>
        </Card>
      )}
      <Stack direction="row" spacing={2}>
        {faces.map((face, idx) => (
          <EmotionBar key={idx} probabilities={face.emotion?.probabilities || {}} />
        ))}
      </Stack>
    </Stack>
  );
}
