import Link from '@mui/material/Link';
import Stack from '@mui/material/Stack';
import { useFetch } from '../../Auth';
import GenerateCodeForm from './GenerateCodeForm';

export default function GenerateCode() {
    const [result, sendRequest] = useFetch('/url', 'POST', null);

    const encodeUrl = async (url) => {
        await sendRequest({ url });
    };

    return (
        <Stack spacing={2} alignItems="center">
            <GenerateCodeForm onSubmit={encodeUrl} />
            {!!result && <Link href={result.url}>{result.url}</Link>}
        </Stack>
    );
}
