import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';

export default function AppBar({ action }) {
    return (
        <MuiAppBar position="static">
            <Toolbar>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    Url Shortener
                </Typography>
                {action}
            </Toolbar>
        </MuiAppBar>
    );
}
