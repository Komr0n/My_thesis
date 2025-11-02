import { useState } from 'react';
import { Box, Card, CardContent, Slider, Stack, Typography } from '@mui/material';

import CameraView from '../components/CameraView';

export default function LivePage() {
  const [threshold, setThreshold] = useState(0.6);
  const [topK, setTopK] = useState(3);

  return (
    <Stack spacing={3} alignItems="center">
      <Typography variant="h4">Live Camera</Typography>
      <Card sx={{ width: '100%', maxWidth: 960, backgroundColor: 'rgba(15,23,42,0.7)' }}>
        <CardContent>
          <CameraView topK={topK} threshold={threshold} />
        </CardContent>
      </Card>
      <Box sx={{ width: '100%', maxWidth: 640 }}>
        <Typography variant="subtitle2">Recognition Threshold: {threshold.toFixed(2)}</Typography>
        <Slider value={threshold} min={0.3} max={0.9} step={0.01} onChange={(_, value) => setThreshold(value as number)} />
        <Typography variant="subtitle2">Top K Matches: {topK}</Typography>
        <Slider value={topK} min={1} max={5} step={1} onChange={(_, value) => setTopK(value as number)} />
      </Box>
    </Stack>
  );
}
