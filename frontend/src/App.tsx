import { useMemo } from 'react';
import { Navigate, Route, Routes, useLocation } from 'react-router-dom';
import { AppBar, Box, CssBaseline, Tab, Tabs, Toolbar, Typography } from '@mui/material';

import LivePage from './pages/Live';
import PhotoPage from './pages/Photo';
import EnrollPage from './pages/Enroll';
import AboutPage from './pages/About';

const routes = [
  { path: '/live', label: 'Live', element: <LivePage /> },
  { path: '/photo', label: 'Photo', element: <PhotoPage /> },
  { path: '/enroll', label: 'Enroll', element: <EnrollPage /> },
  { path: '/about', label: 'About', element: <AboutPage /> }
];

function App() {
  const location = useLocation();
  const activeTab = useMemo(() => {
    const match = routes.find((route) => location.pathname.startsWith(route.path));
    return match ? match.path : false;
  }, [location.pathname]);

  return (
    <Box sx={{ minHeight: '100vh', backgroundColor: '#0f172a', color: '#fff' }}>
      <CssBaseline />
      <AppBar position="static" color="transparent" sx={{ backdropFilter: 'blur(4px)', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Face Emotion Intelligence
          </Typography>
          <Tabs value={activeTab} textColor="inherit" indicatorColor="secondary">
            {routes.map((route) => (
              <Tab key={route.path} value={route.path} label={route.label} href={route.path} />
            ))}
          </Tabs>
        </Toolbar>
      </AppBar>
      <Box component="main" sx={{ p: 2 }}>
        <Routes>
          {routes.map((route) => (
            <Route key={route.path} path={route.path} element={route.element} />
          ))}
          <Route path="/" element={<Navigate to="/live" replace />} />
        </Routes>
      </Box>
    </Box>
  );
}

export default App;
