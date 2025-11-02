import { useState } from 'react';
import { Card, CardContent, Stack, Typography } from '@mui/material';

import LatencyBadge from '../components/LatencyBadge';
import PhotoUpload from '../components/PhotoUpload';

export default function PhotoPage() {
  const [latency, setLatency] = useState<number>();
  return (
    <Stack spacing={3} alignItems="center">
      <Typography variant="h4">Photo Analysis</Typography>
      <Card sx={{ width: '100%', maxWidth: 960, backgroundColor: 'rgba(15,23,42,0.7)' }}>
        <CardContent>
          <PhotoUpload onLatency={setLatency} />
        </CardContent>
      </Card>
      <LatencyBadge latency={latency} />
    </Stack>
  );
}
