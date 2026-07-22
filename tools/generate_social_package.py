from __future__ import annotations

import argparse
import math
import subprocess
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from imageio_ffmpeg import get_ffmpeg_exe

W, H, FPS, RATE = 1080, 1920, 30, 44100
FB = Path(r"C:\Windows\Fonts\arialbd.ttf")
FR = Path(r"C:\Windows\Fonts\arial.ttf")

PACKS = {
    "chuva": {
        "badge":"GUIA DE SEGURANÇA", "feed":"MOTO NA CHUVA\nSEM PRESSA", "story":"CHUVA EXIGE\nMAIS MARGEM", "cover":"PILOTAR NA CHUVA", "cta":"CONFIRA O CHECKLIST COMPLETO",
        "scenes":[("ANTES DE SAIR", "CHUVA NÃO É ROTINA", "Pista molhada reduz aderência e visibilidade."), ("PNEUS", "OLHE OS SULCOS", "Pressão e desgaste merecem checagem antes do trajeto."), ("FREIOS", "COMANDOS SUAVES", "Teste em baixa velocidade, com a moto equilibrada."), ("VISIBILIDADE", "VER E SER VISTO", "Viseira limpa, luzes e sinalização com antecedência."), ("TRAJETO", "MENOS VELOCIDADE", "Mais distância cria tempo para decidir com segurança."), ("EQUIPAMENTO", "PROTEÇÃO QUE FUNCIONA", "Capa, luvas e calçado sem limitar os movimentos.")],
        "images":["guia-pilotar-moto-chuva-capa.jpg","guia-pilotar-moto-chuva-pneu.jpg","guia-pilotar-moto-chuva-capa.jpg","guia-pilotar-moto-chuva-equipamentos.jpg","guia-pilotar-moto-chuva-pneu.jpg","guia-pilotar-moto-chuva-equipamentos.jpg"]},
    "corrente": {
        "badge":"GARAGE TECH", "feed":"CORRENTE DE MOTO:\nCUIDADO CERTO", "story":"CORRENTE LIMPA,\nMOTO SEGURA", "cover":"CUIDE DA CORRENTE", "cta":"VEJA O ROTEIRO SEGURO", 
        "scenes":[("GARAGE TECH", "NÃO É SÓ ESTÉTICA", "Corrente, coroa e pinhão formam um conjunto."), ("INSPEÇÃO", "COMECE PELA FOLGA", "A medida correta está no manual do seu modelo."), ("LIMPEZA", "MOTO SEMPRE PARADA", "Nada de ligar o motor para girar a roda."), ("PRODUTO", "EVITE IMPROVISOS", "Use produto compatível com correntes seladas."), ("LUBRIFICAÇÃO", "POUCO E NO LUGAR CERTO", "Excesso acumula poeira e não protege melhor."), ("DESGASTE", "HORA DE PROCURAR OFICINA", "Elos travados e dentes deformados pedem avaliação.")],
        "images":["garage-tech-corrente-capa.jpg","garage-tech-corrente-capa.jpg","garage-tech-corrente-limpeza.jpg","garage-tech-corrente-limpeza.jpg","garage-tech-corrente-lubrificacao.jpg","garage-tech-corrente-capa.jpg"]},
}

def f(n, bold=False): return ImageFont.truetype(str(FB if bold else FR), n)
def fit(im, sz, fy=.5):
    s=max(sz[0]/im.width, sz[1]/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.Resampling.LANCZOS)
    x=(im.width-sz[0])//2; y=round((im.height-sz[1])*fy); return im.crop((x,y,x+sz[0],y+sz[1]))
def logo(canvas, im, width, y=62):
    r=width/im.width; z=im.resize((width,round(im.height*r)),Image.Resampling.LANCZOS); canvas.alpha_composite(z,((W-z.width)//2,y))
def center(d,text,y,size,color="white",width=900):
    lines=[]; cur=""; ff=f(size,True)
    for word in text.split():
        test=(cur+" "+word).strip()
        if cur and d.textbbox((0,0),test,font=ff,stroke_width=2)[2]>width: lines.append(cur); cur=word
        else: cur=test
    if cur: lines.append(cur)
    for line in lines:
        b=d.textbbox((0,0),line,font=ff,stroke_width=2); d.text(((W-(b[2]-b[0]))//2,y),line,font=ff,fill=color,stroke_width=2,stroke_fill=(0,0,0)); y+=b[3]-b[1]+12
    return y
def scene(src,logo_im,out,badge,head,detail,credit):
    with Image.open(src) as p:
        bg=ImageEnhance.Brightness(fit(p.convert("RGB"),(W,H),.45).filter(ImageFilter.GaussianBlur(28))).enhance(.30).convert("RGBA")
        photo=fit(p.convert("RGB"),(W,940),.48).convert("RGBA")
    bg.alpha_composite(photo,(0,310)); d=ImageDraw.Draw(bg); d.rectangle((0,0,W,300),fill=(3,10,14,215)); d.rounded_rectangle((54,1135,1026,1740),40,fill=(3,10,14,236),outline=(0,215,185),width=4)
    logo(bg,logo_im,510); bf=f(30,True); bb=d.textbbox((0,0),badge,font=bf); pw=bb[2]+54; d.rounded_rectangle(((W-pw)//2,205,(W+pw)//2,262),28,fill=(0,215,185)); d.text(((W-bb[2])//2,216),badge,font=bf,fill=(0,24,28))
    y=center(d,head,1235,64); d.rectangle((410,y+10,670,y+18),fill=(0,215,185)); center(d,detail,y+48,35,(210,238,237),830); d.text((54,1800),credit,font=f(23),fill=(200,210,210)); bg.convert("RGB").save(out,"JPEG",quality=92,optimize=True)
def artwork(src,logo_im,out,badge,text,vertical):
    size=(W,H) if vertical else (W,1350)
    with Image.open(src) as p: can=fit(p.convert("RGB"),size,.45).convert("RGBA")
    ov=Image.new("RGBA",size,(0,0,0,0)); od=ImageDraw.Draw(ov); od.rectangle((0,int(size[1]*.45),size[0],size[1]),fill=(2,10,14,220)); can.alpha_composite(ov); logo(can,logo_im,520 if vertical else 480,60 if vertical else 45); d=ImageDraw.Draw(can); bf=f(31,True); d.rounded_rectangle((55,int(size[1]*.58),55+min(600,d.textbbox((0,0),badge,font=bf)[2]+50),int(size[1]*.58)+58),29,fill=(0,215,185)); d.text((80,int(size[1]*.58)+11),badge,font=bf,fill=(0,24,28)); y=center(d,text,int(size[1]*.68),72 if vertical else 76,width=900); d.text((60,min(y+30,size[1]-100)),"TVDUASRODAS.COM",font=f(32,True),fill=(205,240,237)); can.convert("RGB").save(out,"JPEG",quality=92,optimize=True)
def audio(path,seconds):
    n=int(RATE*seconds); t=np.arange(n)/RATE; a=np.zeros(n)
    for i,start in enumerate(np.arange(0,seconds,2.0)):
        m=(t>=start)&(t<min(start+2,seconds)); q=t[m]-start; chord=((110,165,220),(98,147,196),(87,131,175))[i%3]; a[m]+=sum(np.sin(2*np.pi*x*q) for x in chord)/len(chord)*.12
    for start in np.arange(0,seconds,.5):
        j=int(start*RATE); z=np.arange(min(int(.16*RATE),n-j))/RATE; a[j:j+len(z)]+=np.sin(2*np.pi*(75-32*z)*z)*np.exp(-25*z)*.18
    a/=max(np.max(np.abs(a)),1e-5); a*=.45; fade=int(.35*RATE); a[:fade]*=np.linspace(0,1,fade); a[-fade:]*=np.linspace(1,0,fade); pcm=np.int16(a*32767); stereo=np.column_stack((pcm,pcm)).ravel()
    with wave.open(str(path),'wb') as w: w.setnchannels(2);w.setsampwidth(2);w.setframerate(RATE);w.writeframes(stereo.tobytes())
def video(images,out,seconds=15.0):
    wav=out.with_suffix('.original-track.wav'); audio(wav,seconds); ff=get_ffmpeg_exe(); cmd=[ff,'-y','-loop','1','-i',str(images[0]),'-i',str(wav),'-t',str(seconds),'-r','30','-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)]; subprocess.run(cmd,check=True); wav.unlink()
def reel(scenes,out):
    secs=4; dur=secs*len(scenes); wav=out.with_suffix('.original-track.wav'); audio(wav,dur); ff=get_ffmpeg_exe(); cmd=[ff,'-y']
    for s in scenes: cmd += ['-loop','1','-t',str(secs),'-i',str(s)]
    cmd += ['-i',str(wav)]; filters=[]
    for i in range(len(scenes)): filters.append(f'[{i}:v]scale={W}:{H},zoompan=z=\'min(zoom+0.0007,1.07)\':d=120:s={W}x{H}:fps=30,setsar=1[v{i}]')
    prev='v0'
    for i in range(1,len(scenes)):
        label='out' if i==len(scenes)-1 else f'x{i}'; filters.append(f'[{prev}][v{i}]xfade=transition=fade:duration=0.35:offset={i*3.65:.2f}[{label}]'); prev=label
    cmd += ['-filter_complex',';'.join(filters),'-map','[out]','-map',f'{len(scenes)}:a','-t',f'{dur-0.35*(len(scenes)-1):.2f}','-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)]; subprocess.run(cmd,check=True); wav.unlink()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--pack',choices=PACKS);ap.add_argument('--assets',type=Path,required=True);ap.add_argument('--logo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True); args=ap.parse_args(); p=PACKS[args.pack];args.out.mkdir(parents=True,exist_ok=True)
    with Image.open(args.logo) as x: li=x.convert('RGBA'); artwork(args.assets/p['images'][0],li,args.out/'feed.jpg',p['badge'],p['feed'],False); artwork(args.assets/p['images'][0],li,args.out/'story.jpg',p['badge'],p['story'],True); video([args.out/'story.jpg'],args.out/'story.mp4')
    ss=[]
    for i,((badge,head,detail),name) in enumerate(zip(p['scenes'],p['images']),1):
        o=args.out/f'reel-scene-{i:02d}.jpg'; scene(args.assets/name,li,o,badge,head,detail,'Ilustração editorial gerada por IA');ss.append(o)
    c=args.out/'reel-cover.jpg'; c.write_bytes(ss[0].read_bytes()); reel(ss,args.out/'reel.mp4')
if __name__=='__main__': main()
