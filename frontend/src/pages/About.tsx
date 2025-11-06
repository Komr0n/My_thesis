import { Card, CardContent, List, ListItem, ListItemText, Stack, Typography } from '@mui/material';

export default function AboutPage() {
  return (
    <Stack spacing={3} alignItems="center">
      <Typography variant="h4">About</Typography>
      <Card sx={{ width: '100%', maxWidth: 720, backgroundColor: 'rgba(15,23,42,0.7)' }}>
        <CardContent>
          <Typography variant="h6">Mission</Typography>
          <Typography variant="body1" paragraph>
            Face Emotion Intelligence showcases a privacy-first approach to real-time face analytics.
            Inference happens locally via FastAPI and ONNX Runtime while the PWA provides an installable experience across devices.
          </Typography>
          <Typography variant="h6">Ethics & Privacy</Typography>
          <List>
            <ListItem>
              <ListItemText primary="Consent-driven" secondary="Only enroll identities with explicit permission." />
            </ListItem>
            <ListItem>
              <ListItemText primary="Data minimization" secondary="Store embeddings only, never raw images." />
            </ListItem>
            <ListItem>
              <ListItemText primary="Transparency" secondary="Disclose model limitations and potential bias." />
            </ListItem>
          </List>
          <Typography variant="body2" color="text.secondary">
            Build time: {typeof __BUILD_TIME__ !== 'undefined' ? __BUILD_TIME__ : 'dev'}
          </Typography>
        </CardContent>
      </Card>
    </Stack>
  );
}
