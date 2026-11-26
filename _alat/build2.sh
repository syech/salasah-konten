set -e
F="fps=30,format=yuv420p,setsar=1"
# seg1: sampul Melayu Deli (animasi asli) + zoom pelan, 4.4s
ffmpeg -v error -y -i raw-melayu.mp4 -loop 1 -i a1.png -loop 1 -i a2.png -filter_complex "
[0:v]trim=0:4.4,setpts=PTS-STARTPTS,scale=2160:3840,zoompan=z='1+0.10*on/132':x='iw/2-iw/zoom/2':y='(ih/2+(2756-ih/2)*on/132*0.55)-ih/zoom/2':d=1:s=1080x1920:fps=30[v];
[1:v]format=rgba,fade=in:st=0.2:d=0.45:alpha=1,fade=out:st=2.15:d=0.3:alpha=1[t1];
[2:v]format=rgba,fade=in:st=2.5:d=0.45:alpha=1[t2];
[v][t1]overlay=0:'max(0,24-(t-0.2)*60)'[x];[x][t2]overlay=0:'if(lt(t,2.5),24,max(0,24-(t-2.5)*60))',$F" -t 4.4 -an seg1.mp4
# seg2: montase 4 tema, 1.5s tiap tema, zoom ke nama
i=0
for pair in "jawa-keraton:1651" "tionghoa-classic:1537" "oman:975" "persian-garden:1585"; do
 t=${pair%%:*}; y=${pair##*:}; yy=$((y*2))
 ffmpeg -v error -y -loop 1 -t 1.5 -i shot-$t.png -filter_complex "[0:v]scale=2160:3840,zoompan=z='1.04+0.16*on/44':x='iw/2-iw/zoom/2':y='max(0,min(ih-ih/zoom,(ih/2+($yy-ih/2)*0.6*on/44)-ih/zoom/2))':d=45:s=1080x1920:fps=30,$F" -frames:v 45 -an m$i.mp4
 i=$((i+1))
done
printf "file 'm0.mp4'\nfile 'm1.mp4'\nfile 'm2.mp4'\nfile 'm3.mp4'\n" > mlist.txt
ffmpeg -v error -y -f concat -safe 0 -i mlist.txt -c copy mont-raw.mp4
ffmpeg -v error -y -i mont-raw.mp4 -loop 1 -i a3.png -loop 1 -i a4.png -filter_complex "
[1:v]format=rgba,fade=in:st=0.1:d=0.4:alpha=1,fade=out:st=2.75:d=0.25:alpha=1[t1];[2:v]format=rgba,fade=in:st=3.05:d=0.4:alpha=1[t2];
[0:v][t1]overlay=0:'max(0,24-(t-0.1)*60)':enable='lt(t,3.0)'[x];[x][t2]overlay=0:'if(lt(t,3.05),24,max(0,24-(t-3.05)*60))':enable='gte(t,3.0)',$F" -t 6 -an seg2.mp4
# seg3: end card animasi 3.4s
ffmpeg -v error -y -f lavfi -i color=c=0x1E2F5C:s=1080x1920:d=3.4:r=30 -loop 1 -i e1.png -loop 1 -i e2.png -loop 1 -i e3.png -filter_complex "
[1:v]format=rgba,fade=in:st=0.1:d=0.5:alpha=1[l];[2:v]format=rgba,fade=in:st=0.5:d=0.6:alpha=1[h];[3:v]format=rgba,fade=in:st=1.1:d=0.5:alpha=1[c];
[0:v][l]overlay=0:0[x];[x][h]overlay=0:'max(0,30-(t-0.5)*60)'[y];[y][c]overlay=0:'max(0,30-(t-1.1)*60)',$F" -t 3.4 -an seg3.mp4
# gabung: crossfade halus
ffmpeg -v error -y -i seg1.mp4 -i seg2.mp4 -i seg3.mp4 -f lavfi -i anullsrc=r=44100:cl=stereo -filter_complex "
[0:v]settb=1/30[a];[1:v]settb=1/30[b];[2:v]settb=1/30[c];
[a][b]xfade=transition=fade:duration=0.35:offset=4.05[ab];[ab][c]xfade=transition=fade:duration=0.5:offset=9.6,format=yuv420p[v]" -map "[v]" -map 3:a -c:v libx264 -preset veryfast -crf 18 -c:a aac -b:a 128k -shortest -t 13.0 -movflags +faststart reel-01-v2.mp4
