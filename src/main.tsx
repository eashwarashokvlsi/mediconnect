import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Activity, Bell, CalendarDays, HeartPulse, ShieldCheck, Stethoscope, Video } from 'lucide-react';
import './styles.css';

type Reading = { heartRate: number; spo2: number; temperature: number; at: string };
const seed: Reading = { heartRate: 76, spo2: 98, temperature: 36.8, at: new Date().toISOString() };

function App() {
  const [reading, setReading] = useState(seed);
  const [role, setRole] = useState<'Patient' | 'Doctor'>('Patient');
  const [booked, setBooked] = useState(false);
  useEffect(() => {
    const timer = setInterval(() => setReading({
      heartRate: Math.round(72 + Math.random() * 12),
      spo2: Math.round(96 + Math.random() * 3),
      temperature: Number((36.5 + Math.random() * .6).toFixed(1)),
      at: new Date().toISOString()
    }), 3200);
    return () => clearInterval(timer);
  }, []);
  const status = useMemo(() => reading.heartRate > 120 || reading.spo2 < 94 || reading.temperature > 38 ? 'Attention' : 'Stable', [reading]);
  return <div className="shell">
    <aside>
      <div className="brand"><span className="brandmark"><HeartPulse size={23}/></span><span>MediConnect</span></div>
      <nav aria-label="Primary">
        <a className="active" href="#overview"><Activity size={18}/>Overview</a>
        <a href="#appointments"><CalendarDays size={18}/>Appointments</a>
        <a href="#consult"><Video size={18}/>Consultation</a>
        <a href="#safety"><ShieldCheck size={18}/>Safety</a>
      </nav>
      <div className="privacy"><ShieldCheck size={19}/><div><strong>Demo workspace</strong><small>Synthetic health data only</small></div></div>
    </aside>
    <main>
      <header><div><p className="eyebrow">REMOTE CARE CENTER</p><h1>Good evening, Eashwar</h1><p>Here is today’s connected-care snapshot.</p></div><div className="header-actions"><button className="icon" aria-label="Notifications"><Bell size={20}/><i/></button><button className="role" onClick={() => setRole(role === 'Patient' ? 'Doctor' : 'Patient')}><Stethoscope size={17}/>{role} view</button></div></header>
      <section className="hero" id="overview"><div><span className={`pill ${status.toLowerCase()}`}>{status} · live</span><h2>Your vitals are looking steady.</h2><p>Wearable readings refresh automatically. Your care team is alerted when a measurement crosses a configured threshold.</p><span className="updated">Updated {new Date(reading.at).toLocaleTimeString()}</span></div><div className="orb"><HeartPulse size={46}/><span>LIVE</span></div></section>
      <section className="vitals" aria-label="Current vitals">
        <Metric label="Heart rate" value={String(reading.heartRate)} unit="bpm" range="60–100" tone="coral" />
        <Metric label="Blood oxygen" value={String(reading.spo2)} unit="%" range="95–100" tone="blue" />
        <Metric label="Temperature" value={reading.temperature.toFixed(1)} unit="°C" range="36.1–37.2" tone="amber" />
      </section>
      <section className="grid">
        <article className="panel" id="appointments"><div className="panel-title"><div><span className="kicker">NEXT APPOINTMENT</span><h3>Dr. Maya Patel</h3></div><span className="avatar">MP</span></div><p className="specialty">Cardiology · Video consultation</p><div className="datebox"><CalendarDays size={20}/><div><strong>18 October, 10:30 AM</strong><span>30-minute follow-up</span></div></div><button className="primary" onClick={() => setBooked(true)}>{booked ? 'Appointment confirmed' : 'Confirm appointment'}</button></article>
        <article className="panel" id="consult"><div className="panel-title"><div><span className="kicker">CARE ACTIVITY</span><h3>Monitoring timeline</h3></div><Activity size={22}/></div><ul className="timeline"><li><b>Vitals received</b><span>All measurements within range · now</span></li><li><b>Daily summary prepared</b><span>Available to your assigned doctor · 6:00 PM</span></li><li><b>Medication check-in</b><span>Completed · 9:15 AM</span></li></ul></article>
      </section>
      <footer id="safety">MediConnect is an academic demonstration and is not a medical device. For an emergency, contact local emergency services.</footer>
    </main>
  </div>
}

function Metric({label,value,unit,range,tone}:{label:string,value:string,unit:string,range:string,tone:string}) {
  return <article className={`metric ${tone}`}><div><span>{label}</span><strong>{value}<small>{unit}</small></strong></div><Activity size={29}/><p>Typical range {range}</p></article>
}

createRoot(document.getElementById('root')!).render(<React.StrictMode><App/></React.StrictMode>);

