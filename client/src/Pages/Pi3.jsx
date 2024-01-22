
import React, {useEffect,useState} from 'react';
import DeviceCard from '../Components/DeviceCard';

function PI3() {
  const [fromTimestamp, setFromTimestamp] = useState(0);
  const [toTimestamp, setToTimestamp] = useState(0);

  useEffect(() => {
    const now = new Date();
    const oneHourAgo = new Date(now.getTime() - 60 * 60 * 1000); // Subtract 1 hour in milliseconds

    setFromTimestamp(oneHourAgo.getTime());
    setToTimestamp(now.getTime());
  }, []);

  return (
    <div 
      style={{
      display: "flex",
      width: "100%",
      alignItems: "center",
      justifyContent: "center",
      flexDirection: "column",
    }}>

      <DeviceCard
        label={"PIR - Room4"}
        graph={
          <iframe 
            src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=22`}
            width="450" 
            height="200"
            frameborder="0"
            ></iframe>
        }
      />
      <DeviceCard
        label={"DHT - Room4"}
        graph={
          <iframe src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=24`} width="450" height="200" frameborder="0"></iframe>
        }
        graph2={
          <iframe src={`http://localhost:3000/d-solo/a0effb4f-4d09-48f4-9de3-af7f4cc1bbed/iot?orgId=1&from=${fromTimestamp}&to=${toTimestamp}&panelId=23`} width="450" height="200" frameborder="0"></iframe>
        }
      />
      <DeviceCard
        label={"BB - Bedroom"}
      />
      <DeviceCard
        label={"B4SD - Bedroom"}
      />
      <DeviceCard
        label={"IR - Bedroom"}
      />
      <DeviceCard
        label={"RGB - Bedroom"}
      />
    </div>
  );
}

export default PI3;
