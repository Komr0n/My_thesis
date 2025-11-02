import { Box, LinearProgress, Stack, Typography } from '@mui/material';

interface EmotionBarProps {
  probabilities: Record<string, number>;
}

export default function EmotionBar({ probabilities }: EmotionBarProps) {
  const entries = Object.entries(probabilities || {}).sort((a, b) => b[1] - a[1]);
  return (
    <Stack spacing={0.5} sx={{ width: '200px' }}>
      {entries.map(([label, value]) => (
        <Box key={label}>
          <Stack direction="row" justifyContent="space-between">
            <Typography variant="caption">{label}</Typography>
            <Typography variant="caption">{Math.round(value * 100)}%</Typography>
          </Stack>
          <LinearProgress variant="determinate" value={value * 100} sx={{ height: 6, borderRadius: 2 }} />
        </Box>
      ))}
    </Stack>
  );
}
