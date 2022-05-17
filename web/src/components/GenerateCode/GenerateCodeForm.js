import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import TextField from '@mui/material/TextField';
import { useState } from 'react';

export default function GenerateCodeForm({ onSubmit }) {
    const [url, setUrl] = useState('');

    const submit = () => onSubmit(url);

    return (
        <Container>
            <TextField
                autoFocus
                id="url"
                margin="dense"
                label="URL"
                type="text"
                fullWidth
                required
                variant="standard"
                placeholder="https://www.google.com"
                value={url}
                onChange={(ev) => setUrl(ev.target.value)}
            />
            <Button variant="contained" onClick={submit}>
                Shorten
            </Button>
        </Container>
    );
}
