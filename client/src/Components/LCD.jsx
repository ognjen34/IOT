
import { Typography } from '@mui/material';
import {React,useEffect,useState} from 'react';
import io from "socket.io-client";

function LCD() {
    const [temperature,setTemperature] = useState("0")
    const [humidity,setHumidity] = useState("0")

    useEffect(() => {
        const socket = io.connect("http://localhost:5000");
        
    
        socket.on("temperature", (data) => {
          console.log("Temperature:", data);
          setTemperature(data)
        });
    
        socket.on("humidity", (data) => {
          console.log("Humidity:", data);
          setHumidity(data)
        });
    
    
    
        return () => {
          socket.disconnect();
        };
      }, []);

  return (
    <div >
        <Typography>Current Humidity : {humidity}</Typography>
        <Typography>Current Temperature : {temperature}</Typography>

    </div>
  );
}

export default LCD;
