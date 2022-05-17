import { createContext, useCallback, useContext, useState } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [token, setToken] = useState(null);

    const auth = {
        isAuthenticated: !!token,
        token,
        setToken,
    };

    return <AuthContext.Provider value={auth}>{children}</AuthContext.Provider>;
}

export const useAuth = () => useContext(AuthContext);

export const useLoginWithEmailAndPassword = () => {
    const { token, setToken } = useAuth();

    const loginWithEmailAndPassword = useCallback(
        async ({ email, password }) => {
            try {
                const response = await fetch(
                    'http://localhost:8000/user/token',
                    {
                        method: 'POST',
                        body: new URLSearchParams({
                            username: email,
                            password,
                        }),
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );
                const result = await response.json();
                const accessToken = result['access_token'];
                setToken(accessToken);
            } catch (error) {
                // Handle error
                console.error(error);
            }
        },
        [token, setToken]
    );

    return loginWithEmailAndPassword;
};

export const useLogout = () => {
    const { token, setToken } = useAuth();

    const logout = useCallback(async () => {
        if (token === null) return;
        try {
            await fetch('http://localhost:8000/user/logout', {
                method: 'POST',
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
        } catch (error) {
            console.error(error);
        } finally {
            setToken(null);
        }
    }, [token, setToken]);

    return logout;
};

export const useFetch = (path, method, initialValue) => {
    const [value, setValue] = useState(initialValue);

    const { token } = useAuth();

    const sendRequest = useCallback(
        async (data) => {
            // TODO: handle unauthenticated case
            const response = await fetch(`http://localhost:8000${path}`, {
                method,
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: token && `Bearer ${token}`,
                },
            });
            const result = await response.json();
            setValue(result);
        },
        [token, setValue, path, method]
    );

    return [value, sendRequest];
};
