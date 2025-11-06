import { Chip } from '@mui/material';

interface LatencyBadgeProps {
  latency?: number;
}

export default function LatencyBadge({ latency }: LatencyBadgeProps) {
  const label = latency ? `${latency.toFixed(0)} ms` : '—';
  return <Chip label={`Latency ${label}`} color="secondary" variant="outlined" size="small" />;
}
