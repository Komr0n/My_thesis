import { ChangeEvent, useState } from 'react';
import { Button, Dialog, DialogActions, DialogContent, DialogTitle, LinearProgress, Stack, TextField, Typography } from '@mui/material';

import { enrollPerson } from '../api/client';

interface EnrollDialogProps {
  open: boolean;
  onClose: () => void;
}

export default function EnrollDialog({ open, onClose }: EnrollDialogProps) {
  const [name, setName] = useState('');
  const [notes, setNotes] = useState('');
  const [images, setImages] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFiles = async (event: ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || []);
    const readers = await Promise.all(
      files.map(
        (file) =>
          new Promise<string>((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result as string);
            reader.onerror = () => reject(reader.error);
            reader.readAsDataURL(file);
          })
      )
    );
    setImages(readers);
  };

  const handleSubmit = async () => {
    if (!name || images.length === 0) {
      setError('Name and at least one image are required');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const response = await enrollPerson(name, images, notes);
      setResult(`Enrolled ${response.name} (#${response.person_id})`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Enrollment failed');
    } finally {
      setLoading(false);
    }
  };

  const closeDialog = () => {
    setName('');
    setNotes('');
    setImages([]);
    setResult(null);
    setError(null);
    onClose();
  };

  return (
    <Dialog open={open} onClose={closeDialog} fullWidth maxWidth="sm">
      <DialogTitle>Enroll New Person</DialogTitle>
      <DialogContent>
        <Stack spacing={2} sx={{ mt: 1 }}>
          <TextField label="Name" value={name} onChange={(event) => setName(event.target.value)} fullWidth />
          <TextField
            label="Notes"
            value={notes}
            onChange={(event) => setNotes(event.target.value)}
            fullWidth
            multiline
            rows={2}
          />
          <Button variant="outlined" component="label">
            Select Photos
            <input hidden accept="image/*" type="file" multiple onChange={handleFiles} />
          </Button>
          <Typography variant="caption">Selected {images.length} images</Typography>
          {loading && <LinearProgress />}
          {error && (
            <Typography color="error" variant="body2">
              {error}
            </Typography>
          )}
          {result && <Typography color="success.main">{result}</Typography>}
        </Stack>
      </DialogContent>
      <DialogActions>
        <Button onClick={closeDialog}>Close</Button>
        <Button onClick={handleSubmit} disabled={loading} variant="contained">
          Enroll
        </Button>
      </DialogActions>
    </Dialog>
  );
}
