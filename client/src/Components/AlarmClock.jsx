import { React, useEffect ,useState} from "react";
import AccessAlarmIcon from '@mui/icons-material/AccessAlarm';
import axios from "axios";
import io from "socket.io-client";


function AlarmClock() {

    const [alarm, setAlarm] = useState("blue");


    useEffect(() => {
        const socket = io.connect("http://localhost:5000");
        socket.on("alarmClock", (data) => {
          console.log("Received message from server:", data);
          setAlarm(data);
        });
    
        return () => {
          socket.disconnect();
        };
      }, []);




    const alarmClockOff = () =>{
        axios.post("http://localhost:5000/b4sd", {mode:"alarmClockOff"})
            .then(response => {
                console.log(response.data);
            })
            .catch(error => {
                console.error(error);
            });
    }

    return(
        <div>
            <AccessAlarmIcon
                onClick={alarmClockOff}
               sx={{color:alarm, fontSize:"50px", cursor:"pointer"}} 
            />
        </div>
    );
}

export default AlarmClock;