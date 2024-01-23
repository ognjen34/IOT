import { React, useEffect ,useState} from "react";
import { Typography, Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField } from "@mui/material";
import axios from "axios";

function Clock(){
    const locale = 'en';
    const [today, setDate] = useState(new Date()); 
    const [openDialog, setOpenDialog] = useState(false);
    const [hours, setHours] = useState(0);
    const [minutes, setMinutes] = useState(0);


    useEffect(() => {
        const timer = setInterval(() => { 
        setDate(new Date());
      }, 60*1000);
      return () => {
        clearInterval(timer); 
      }
    }, []);

    const handleOpenDialog = () => {
        setOpenDialog(true);
    };

    const handleCloseDialog = () => {
        setOpenDialog(false);
    };

    const handleSetAlarm = () => {
        const formattedHours = String(hours).padStart(2, '0');
        const formattedMinutes = String(minutes).padStart(2, '0');
        const alarmTime = formattedHours + formattedMinutes;
        // Perform actions when setting the alarm
        console.log("Alarm set:", alarmTime);
        axios.post("http://localhost:5000/b4sd", {mode:alarmTime})
            .then(response => {
                console.log(response.data);
            })
            .catch(error => {
                console.error(error);
            });
        handleCloseDialog();
    };


    const time = today.toLocaleTimeString(locale, { hour: 'numeric', hour12: true, minute: 'numeric'});

    return(
        <div>
            <Typography sx={{fontSize:"50px", fontWeight:"bold"}}>{time}</Typography>
            <Button variant="contained"  onClick={handleOpenDialog}> set alarm</Button>
            <Dialog open={openDialog} onClose={handleCloseDialog}>
                <DialogTitle>Set Alarm</DialogTitle>
                <DialogContent>
                    <div style={{display:"flex", alignItems:"true", justifyContent:"true", padding:"10px"}}> 
                        <TextField
                            sx={{width:"100px", marginRight:"10px"}}
                            label="Hours"
                            type="number"
                            value={hours}
                            onChange={(e) => setHours(e.target.value)}
                            
                        />
                        <p>:</p>
                        <TextField
                            sx={{width:"100px", marginLeft:"10px"}}
                            label="Minutes"
                            type="number"
                            value={minutes}
                            onChange={(e) => setMinutes(e.target.value)}
                            
                        />
                    </div>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseDialog}>Cancel</Button>
                    <Button onClick={handleSetAlarm} variant="contained" color="primary">
                        Set Alarm
                    </Button>
                </DialogActions>
            </Dialog>
        </div>
    )
}

export default Clock;