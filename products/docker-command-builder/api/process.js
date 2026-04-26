// Docker Command Builder - Process API
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { action, params } = req.body;

    if (!action) {
      return res.status(400).json({ error: 'Action is required' });
    }

    let command = '';
    let explanation = '';

    switch (action) {
      case 'run':
        command = buildRunCommand(params);
        explanation = 'Creates and starts a container from an image';
        break;
      case 'build':
        command = buildBuildCommand(params);
        explanation = 'Builds a Docker image from a Dockerfile';
        break;
      case 'compose':
        command = buildComposeCommand(params);
        explanation = 'Docker Compose command for multi-container apps';
        break;
      case 'exec':
        command = buildExecCommand(params);
        explanation = 'Executes a command in a running container';
        break;
      case 'logs':
        command = buildLogsCommand(params);
        explanation = 'Fetches logs from a container';
        break;
      case 'network':
        command = buildNetworkCommand(params);
        explanation = 'Manages Docker networks';
        break;
      case 'volume':
        command = buildVolumeCommand(params);
        explanation = 'Manages Docker volumes';
        break;
      default:
        return res.status(400).json({ error: 'Unknown action' });
    }

    return res.status(200).json({
      command,
      explanation,
      action,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}

function buildRunCommand(params) {
  const {
    image = 'nginx',
    name = '',
    ports = [],
    volumes = [],
    env = [],
    detach = true,
    rm = false,
    interactive = false,
    tty = false,
    restart = 'no',
    memory = '',
    cpus = ''
  } = params;

  let cmd = 'docker run';

  if (detach) cmd += ' -d';
  if (rm) cmd += ' --rm';
  if (interactive) cmd += ' -i';
  if (tty) cmd += ' -t';
  if (name) cmd += ` --name ${name}`;
  if (restart && restart !== 'no') cmd += ` --restart ${restart}`;
  if (memory) cmd += ` --memory=${memory}`;
  if (cpus) cmd += ` --cpus=${cpus}`;

  ports.forEach(p => {
    if (p.host && p.container) {
      cmd += ` -p ${p.host}:${p.container}`;
    }
  });

  volumes.forEach(v => {
    if (v.host && v.container) {
      cmd += ` -v ${v.host}:${v.container}${v.readOnly ? ':ro' : ''}`;
    }
  });

  env.forEach(e => {
    if (e.key) {
      cmd += ` -e ${e.key}${e.value ? `=${e.value}` : ''}`;
    }
  });

  cmd += ` ${image}`;

  return cmd;
}

function buildBuildCommand(params) {
  const {
    path = '.',
    tag = '',
    dockerfile = 'Dockerfile',
    noCache = false,
    buildArgs = [],
    target = '',
    platform = ''
  } = params;

  let cmd = 'docker build';

  if (tag) cmd += ` -t ${tag}`;
  if (dockerfile && dockerfile !== 'Dockerfile') cmd += ` -f ${dockerfile}`;
  if (noCache) cmd += ' --no-cache';
  if (target) cmd += ` --target ${target}`;
  if (platform) cmd += ` --platform ${platform}`;

  buildArgs.forEach(arg => {
    if (arg.key) {
      cmd += ` --build-arg ${arg.key}=${arg.value || ''}`;
    }
  });

  cmd += ` ${path}`;

  return cmd;
}

function buildComposeCommand(params) {
  const {
    action = 'up',
    file = 'docker-compose.yml',
    detached = true,
    build = false,
    service = ''
  } = params;

  let cmd = 'docker-compose';

  if (file && file !== 'docker-compose.yml') {
    cmd += ` -f ${file}`;
  }

  cmd += ` ${action}`;

  if (action === 'up') {
    if (detached) cmd += ' -d';
    if (build) cmd += ' --build';
  }

  if (service) {
    cmd += ` ${service}`;
  }

  return cmd;
}

function buildExecCommand(params) {
  const {
    container = '',
    command = '/bin/sh',
    interactive = true,
    tty = true,
    user = ''
  } = params;

  if (!container) return 'docker exec [container required]';

  let cmd = 'docker exec';

  if (interactive) cmd += ' -i';
  if (tty) cmd += ' -t';
  if (user) cmd += ` -u ${user}`;

  cmd += ` ${container} ${command}`;

  return cmd;
}

function buildLogsCommand(params) {
  const {
    container = '',
    follow = false,
    tail = 0,
    timestamps = false
  } = params;

  if (!container) return 'docker logs [container required]';

  let cmd = 'docker logs';

  if (follow) cmd += ' -f';
  if (timestamps) cmd += ' -t';
  if (tail > 0) cmd += ` --tail ${tail}`;

  cmd += ` ${container}`;

  return cmd;
}

function buildNetworkCommand(params) {
  const { action = 'ls', name = '', driver = 'bridge' } = params;

  switch (action) {
    case 'create':
      return `docker network create${driver !== 'bridge' ? ` --driver ${driver}` : ''}${name ? ` ${name}` : ''}`;
    case 'rm':
      return `docker network rm ${name || '[network name]'}`;
    case 'inspect':
      return `docker network inspect ${name || '[network name]'}`;
    default:
      return 'docker network ls';
  }
}

function buildVolumeCommand(params) {
  const { action = 'ls', name = '', driver = 'local' } = params;

  switch (action) {
    case 'create':
      return `docker volume create${driver !== 'local' ? ` --driver ${driver}` : ''}${name ? ` ${name}` : ''}`;
    case 'rm':
      return `docker volume rm ${name || '[volume name]'}`;
    case 'inspect':
      return `docker volume inspect ${name || '[volume name]'}`;
    default:
      return 'docker volume ls';
  }
}
