import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import TextField from '@mui/material/TextField';
import { useState } from 'react';

export default function LoginDialog({ open, onSubmit, onClose }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const submit = () => {
        onClose();
        return onSubmit({
            email,
            password,
        });
    };

    return (
        <Dialog open={open} onClose={onClose} keepMounted={false}>
            <DialogTitle>Login</DialogTitle>
            <DialogContent>
                <DialogContentText>
                    To use this service, you need to be authenticated. You can
                    use the placeholders in the text fields to login.
                </DialogContentText>
                <TextField
                    autoFocus
                    id="email"
                    margin="dense"
                    label="Email Address"
                    type="email"
                    fullWidth
                    required
                    variant="standard"
                    value={email}
                    onChange={(ev) => setEmail(ev.target.value)}
                    placeholder="johndoe@example.com"
                />
                <TextField
                    id="password"
                    margin="dense"
                    label="Password"
                    type="password"
                    fullWidth
                    required
                    variant="standard"
                    value={password}
                    onChange={(ev) => setPassword(ev.target.value)}
                    placeholder="secret"
                />
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Cancel</Button>
                <Button onClick={submit} variant="contained">
                    Login
                </Button>
            </DialogActions>
        </Dialog>
    );
}
