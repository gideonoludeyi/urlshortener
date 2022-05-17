import Button from '@mui/material/Button';
import { useState } from 'react';
import { useAuth, useLoginWithEmailAndPassword, useLogout } from './Auth';
import AppBar from './components/AppBar';
import GenerateCode from './components/GenerateCode';
import LoginDialog from './components/LoginDialog';

export default function App() {
    const { isAuthenticated } = useAuth();
    const loginWithEmailAndPassword = useLoginWithEmailAndPassword();
    const logout = useLogout();

    const [loginDialogVisibility, setLoginDialogVisibility] = useState(false);

    const openLoginDialog = () => setLoginDialogVisibility(true);
    const closeLoginDialog = () => setLoginDialogVisibility(false);

    const appBarAction = isAuthenticated ? (
        <Button color="inherit" onClick={logout}>
            Logout
        </Button>
    ) : (
        <Button color="inherit" onClick={openLoginDialog}>
            Login
        </Button>
    );

    return (
        <div>
            <AppBar action={appBarAction} />
            <GenerateCode />

            {/* Hidden */}
            <LoginDialog
                open={loginDialogVisibility}
                onClose={closeLoginDialog}
                onSubmit={loginWithEmailAndPassword}
            />
        </div>
    );
}
