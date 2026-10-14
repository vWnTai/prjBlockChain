import {spawnSync} from 'node:child_process';
import './setup.mjs';
const action=process.argv[2]??'up';
const commands={up:[['config','--quiet'],['up','--build','-d','--wait']],down:[['down']],status:[['ps']],test:[['--profile','test','run','--rm','test']],logs:[['logs','--tail','100','api','worker']]};
if(!(action in commands))throw new Error('Action must be up, down, status, test or logs');
for(const args of commands[action]){const child=spawnSync('docker',['compose',...args],{cwd:new URL('..',import.meta.url),stdio:'inherit'});if(child.status!==0)process.exit(child.status??1)}
