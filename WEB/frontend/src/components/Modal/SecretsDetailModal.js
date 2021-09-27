import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
};

export default function secretsDetailModal(props) {
    const { isOpen, setOpen, title, preview, url, id } = props;
    
    const handleOpen = () => setOpen(true);
    const handleClose = () => setOpen(false);

    return (
        <div>
            {/* <Button onClick={handleOpen}>Open modal</Button>   */}
            <Modal
                open={isOpen}
                onClose={handleClose}
                aria-labelledby="secrets-modal-title"
                aria-describedby="secrets-modal-description"
            >
                <Box sx={style}>
                    <Typography id="secrets-modal-title" variant="h6" component="h2">
                        {title}
                    </Typography>
                    <Typography id="secrets-modal-description" sx={{ mt: 2 }}>
                        {preview}
                    </Typography>
                    <a href={url} />
                    <button>scrap {id}</button>
                </Box>
            </Modal>
        </div>
    );
}