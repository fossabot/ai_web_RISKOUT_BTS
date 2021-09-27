import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import Link from '@mui/material/Link';

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: '50vw',
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
};

export default function secretsDetailModal(props) {
    const { isOpen, setOpen, data, scrapArticle } = props;

    const handleClose = () => setOpen(false);
    return (
        <div>
            <Modal
                open={isOpen}
                onClose={handleClose}
                aria-labelledby="secrets-modal-title"
                aria-describedby="secrets-modal-description"
            >
                <Box sx={style}>
                    <Typography id="secrets-modal-title" variant="h6" component="h2">
                        {data.title}
                    </Typography>
                    <Typography id="secrets-modal-description" sx={{ mt: 2 }}>
                        {data.summarized}
                    </Typography>
                    <Link href={data.site_url} color="inherit" underline="hover" target="_blank">Source</Link>
                    <Link href="#" color="inherit" underline="hover">Page Analysis</Link>
                    <Button onClick={scrapArticle}>Save article</Button>
                </Box>
            </Modal>
        </div>
    );
}
