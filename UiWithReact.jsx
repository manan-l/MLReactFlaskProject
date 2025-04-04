import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  CssBaseline,
  Box,
  Container,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Paper
} from '@mui/material';
import {
  Info as InfoIcon,
  Timeline as TimelineIcon,
  TableChart as TableChartIcon,
  Assessment as AssessmentIcon,
  Login as LoginIcon
} from '@mui/icons-material';

const drawerWidth = 240;

const App = () => {
  const [activeTab, setActiveTab] = useState('intro');
  const [dateInput, setDateInput] = useState('');
  const [hourInput, setHourInput] = useState('00');
  const [minuteInput, setMinuteInput] = useState('00');
  const [gasSelection, setGasSelection] = useState('co');

  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  // Dummy event handlers for demonstration
  const handlePredict = () => {
    // integrate your prediction logic here
    alert(`Predicting AQI for ${dateInput} ${hourInput}:${minuteInput}`);
  };

  const handleViewGraph = () => {
    // integrate your trend analysis logic here
    alert(`Viewing graph for ${gasSelection}`);
  };

  // Sidebar navigation items
  const navItems = [
    { text: 'Introduction', icon: <InfoIcon />, tab: 'intro' },
    { text: 'Predict AQI', icon: <TimelineIcon />, tab: 'predict' },
    { text: 'View Data', icon: <TableChartIcon />, tab: 'data' },
    { text: 'Analysis', icon: <AssessmentIcon />, tab: 'analysis' },
    { text: 'Login', icon: <LoginIcon />, tab: 'login' }
  ];

  // UI for each tab
  const renderContent = () => {
    switch (activeTab) {
      case 'intro':
        return (
          <Box
            sx={{
              height: '100vh',
              backgroundImage: `url('https://images.moneycontrol.com/static-mcnews/2024/11/20241102025036_Delhi-AQI.jpg?impolicy=website&width=770&height=431')`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              textAlign: 'center',
              p: 2
            }}
          >
            <Typography variant="h3" component="h1" sx={{ fontWeight: 'bold' }}>
              Welcome to the Delhi Air Quality Predictor
            </Typography>
            <Typography variant="h6" component="p" sx={{ mt: 2, fontWeight: 'bold' }}>
              The Delhi Air Quality Predictor is an interactive application that empowers users to predict air quality index (AQI) and pollutant concentrations.
            </Typography>
            <Typography variant="h6" component="p" sx={{ mt: 1, fontWeight: 'bold' }}>
              It leverages advanced predictive modeling to provide accurate forecasts based on user-selected dates and times.
            </Typography>
            <Typography variant="h6" component="p" sx={{ mt: 1, fontWeight: 'bold' }}>
              Dynamic visualizations make it easy to explore historical and forecasted trends, enhancing your understanding of air quality patterns.
            </Typography>
            <Typography variant="h6" component="p" sx={{ mt: 1, fontWeight: 'bold' }}>
              This tool is designed for decision-making and awareness in addressing air pollution challenges.
            </Typography>
            <Button variant="contained" color="primary" sx={{ mt: 3 }} onClick={() => handleTabChange('predict')}>
              Get Started
            </Button>
          </Box>
        );
      case 'predict':
        return (
          <Container sx={{ mt: 4 }}>
            <Paper sx={{ p: 3, mb: 4, border: '2px solid #1E90FF', borderRadius: '10px' }}>
              <Typography variant="h5" sx={{ mb: 2 }}>Select Date and Time for Prediction</Typography>
              <TextField
                label="Select Date"
                type="date"
                value={dateInput}
                onChange={(e) => setDateInput(e.target.value)}
                InputLabelProps={{ shrink: true }}
                sx={{ mr: 2 }}
              />
              <FormControl sx={{ mr: 2, minWidth: 120 }}>
                <InputLabel>Hour</InputLabel>
                <Select
                  value={hourInput}
                  label="Hour"
                  onChange={(e) => setHourInput(e.target.value)}
                >
                  {Array.from({ length: 24 }, (_, i) => (
                    <MenuItem key={i} value={i < 10 ? `0${i}` : `${i}`}>
                      {i < 10 ? `0${i}` : `${i}`}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              <FormControl sx={{ mr: 2, minWidth: 120 }}>
                <InputLabel>Minute</InputLabel>
                <Select
                  value={minuteInput}
                  label="Minute"
                  onChange={(e) => setMinuteInput(e.target.value)}
                >
                  {Array.from({ length: 12 }, (_, i) => {
                    const minutes = i * 5;
                    const minuteStr = minutes < 10 ? `0${minutes}` : `${minutes}`;
                    return (
                      <MenuItem key={i} value={minuteStr}>
                        {minuteStr}
                      </MenuItem>
                    );
                  })}
                </Select>
              </FormControl>
              <Button variant="contained" color="success" onClick={handlePredict}>
                Predict AQI
              </Button>
            </Paper>
            <Paper sx={{ p: 3, border: '2px solid #1E90FF', borderRadius: '10px' }}>
              <Typography variant="h5" sx={{ mb: 2 }}>Prediction Results</Typography>
              {/* Replace the below with your results and chart component */}
              <Typography variant="body1" sx={{ mb: 2 }}>
                {/* Example result placeholder */}
                AQI Prediction: [Results will be displayed here]
              </Typography>
              <Box sx={{ height: 300, backgroundColor: '#f0f0f0' }}>
                <Typography variant="body2" align="center" sx={{ pt: 12 }}>
                  Forecast Plot Placeholder
                </Typography>
              </Box>
            </Paper>
          </Container>
        );
      case 'data':
        return (
          <Container sx={{ mt: 4 }}>
            <Paper sx={{ p: 3, border: '2px solid #1E90FF', borderRadius: '10px' }}>
              <Typography variant="h5" sx={{ mb: 2 }}>Air Quality Data</Typography>
              {/* Replace with your data table component */}
              <Typography variant="body1">
                Data Table Placeholder (you can integrate libraries like react-table)
              </Typography>
            </Paper>
          </Container>
        );
      case 'login':
        return (
          <Container sx={{ mt: 4 }}>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
              <Paper sx={{ p: 3, border: '2px solid #1E90FF', borderRadius: '10px' }}>
                <Typography variant="h5" sx={{ mb: 2 }}>Login with Google</Typography>
                <Button variant="contained" color="primary" startIcon={<LoginIcon />}>
                  Login with Google
                </Button>
              </Paper>
              <Paper sx={{ p: 3, border: '2px solid #1E90FF', borderRadius: '10px' }}>
                <Typography variant="h5" sx={{ mb: 2 }}>User Info</Typography>
                {/* Replace with dynamic user information */}
                <Typography variant="body1">
                  User info will be displayed here.
                </Typography>
              </Paper>
            </Box>
          </Container>
        );
      case 'analysis':
        return (
          <Container sx={{ mt: 4 }}>
            <Paper sx={{ p: 3, mb: 4, border: '2px solid #1E90FF', borderRadius: '10px' }}>
              <Typography variant="h5" sx={{ mb: 2 }}>Select Gas or AQI to View Trends</Typography>
              <FormControl sx={{ mr: 2, minWidth: 200 }}>
                <InputLabel>Gas/AQI</InputLabel>
                <Select
                  value={gasSelection}
                  label="Gas/AQI"
                  onChange={(e) => setGasSelection(e.target.value)}
                >
                  {["co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3", "AQI"].map((gas) => (
                    <MenuItem key={gas} value={gas}>
                      {gas.toUpperCase()}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              <Button variant="contained" color="info" onClick={handleViewGraph}>
                View Graph
              </Button>
            </Paper>
            <Paper sx={{ p: 3, border: '2px solid #1E90FF', borderRadius: '10px' }}>
              <Typography variant="h5" sx={{ mb: 2 }}>Gas/AQI Trend Analysis</Typography>
              {/* Replace with your trend plot component */}
              <Box sx={{ height: 400, backgroundColor: '#f0f0f0' }}>
                <Typography variant="body2" align="center" sx={{ pt: 18 }}>
                  Trend Plot Placeholder
                </Typography>
              </Box>
            </Paper>
          </Container>
        );
      default:
        return null;
    }
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          <Typography variant="h6" noWrap>
            Delhi Air Quality Prediction
          </Typography>
          <Button variant="contained" color="error">
            Logout
          </Button>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' }
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <List>
            {navItems.map((item) => (
              <ListItem
                button
                key={item.text}
                onClick={() => handleTabChange(item.tab)}
                selected={activeTab === item.tab}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        {renderContent()}
      </Box>
    </Box>
  );
};

export default App;
