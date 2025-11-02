import { useEffect, useState } from 'react';
import { Button, Card, CardContent, List, ListItem, ListItemText, Stack, Typography } from '@mui/material';

import EnrollDialog from '../components/EnrollDialog';
import { fetchPersons } from '../api/client';

interface PersonRecord {
  id: number;
  name: string;
  notes?: string;
  embedding_count: number;
}

export default function EnrollPage() {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [persons, setPersons] = useState<PersonRecord[]>([]);

  const loadPersons = async () => {
    try {
      const response = await fetchPersons();
      setPersons(response.results);
    } catch (err) {
      // eslint-disable-next-line no-console
      console.error(err);
    }
  };

  useEffect(() => {
    void loadPersons();
  }, []);

  return (
    <Stack spacing={3} alignItems="center">
      <Typography variant="h4">Enrollment</Typography>
      <Button variant="contained" onClick={() => setDialogOpen(true)}>
        Enroll Person
      </Button>
      <Card sx={{ width: '100%', maxWidth: 640, backgroundColor: 'rgba(15,23,42,0.7)' }}>
        <CardContent>
          <Typography variant="h6">Known Persons</Typography>
          <List>
            {persons.map((person) => (
              <ListItem key={person.id} divider>
                <ListItemText primary={person.name} secondary={`Embeddings: ${person.embedding_count}`} />
              </ListItem>
            ))}
          </List>
        </CardContent>
      </Card>
      <EnrollDialog
        open={dialogOpen}
        onClose={() => {
          setDialogOpen(false);
          void loadPersons();
        }}
      />
    </Stack>
  );
}
