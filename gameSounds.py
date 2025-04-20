import math
import random
import stdaudio
import stdarray

def shooting_sound():
    
    sample_rate = 44100
    duration = 0.3
    N = int(sample_rate * duration)
    samples = stdarray.create1D(N, 0.0)

    for i in range(N):
        t = i / sample_rate
        freq = 1200.0 - 1000.0 * (i/N)
        pew = math.sin(2 * math.pi * t * freq)
        noise = (random.random() * 2 - 1) * 0.1
        envelope = 1.0 if i < N/10 else math.exp(-5.0 * (i - N/10)/N)
        samples[i] = envelope * (pew + noise) * 0.5

    stdaudio.playSamples(samples)

def explosion_sound():
    
    sample_rate = 22050  
    duration = 0.5  
    N = int(sample_rate * duration)
    samples = stdarray.create1D(N, 0.0)

    for i in range(N):
        t = i / sample_rate
        
        progress = min(1.0, i/N)  
        freq = max(30.0, 80.0 - 60.0 * progress)  
        
        
        boom = math.sin(2 * math.pi * t * freq)
        crackle = math.sin(2 * math.pi * t * 400) * math.exp(-8.0 * progress)
        noise = (random.random() * 2 - 1) * 0.4 * math.exp(-4.0 * progress)
        
        
        if i < N//8:  
            envelope = i / (N//8)
        else:  
            envelope = math.exp(-12.0 * (i - N//8)/N)
        
        samples[i] = envelope * (boom * 0.6 + crackle * 0.3 + noise) * 0.7

    stdaudio.playSamples(samples)

def gameover_sound():
    
    sample_rate = 44100
    duration = 3.0  
    N = int(sample_rate * duration)
    samples = stdarray.create1D(N, 0.0)

    for i in range(N):
        t = i / sample_rate
        
        freq1 = 400.0 - 350.0 * (i/N)
        freq2 = 600.0 - 500.0 * (i/N)
        wave1 = math.sin(2 * math.pi * t * freq1)
        wave2 = 0.5 * math.sin(2 * math.pi * t * freq2)

        envelope = math.exp(-0.8 * i/N)
        
        wave = wave1 + wave2 + 0.3 * math.sin(2 * math.pi * t * freq1 * 1.5)
        samples[i] = wave * envelope * 0.5

    stdaudio.playSamples(samples)

def youwin_sound():

    sample_rate = 44100
    duration = 3.5  
    N = int(sample_rate * duration)
    samples = stdarray.create1D(N, 0.0)

    for i in range(N):
        t = i / sample_rate
        
        freq1 = 300.0 + 400.0 * (i/N)
        freq2 = 450.0 + 300.0 * (i/N)
        freq3 = 600.0 + 200.0 * (i/N)
        wave1 = math.sin(2 * math.pi * t * freq1)
        wave2 = 0.6 * math.sin(2 * math.pi * t * freq2)
        wave3 = 0.4 * math.sin(2 * math.pi * t * freq3)
               
        envelope = (0.5 + 0.5 * math.sin(2 * math.pi * t * 2)) * math.exp(-0.3 * i/N)
        
        wave = wave1 + wave2 + wave3
        samples[i] = wave * envelope * 0.4

    stdaudio.playSamples(samples)

if __name__ == "__main__":
    main()
