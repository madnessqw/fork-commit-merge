module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { spec, licenseKey } = req.body;

    // License validation placeholder
    if (!licenseKey || licenseKey === 'demo') {
      // Allow demo mode with limited features
    }

    if (!spec) {
      return res.status(400).json({ error: 'No spec provided' });
    }

    let parsedSpec;
    try {
      parsedSpec = typeof spec === 'string' ? JSON.parse(spec) : spec;
    } catch (e) {
      try {
        // Try YAML parsing (basic)
        parsedSpec = require('js-yaml').load(spec);
      } catch (yamlErr) {
        return res.status(400).json({
          valid: false,
          errors: [{ message: 'Invalid JSON/YAML format', line: 1 }],
          summary: { total: 1, errors: 1, warnings: 0 }
        });
      }
    }

    const errors = [];
    const warnings = [];

    // OpenAPI version check
    const openapiVersion = parsedSpec.openapi || parsedSpec.swagger;
    if (!openapiVersion) {
      errors.push({ message: 'Missing openapi/swagger version field', severity: 'error', line: 1 });
    } else if (!['2.0', '3.0.0', '3.0.1', '3.0.2', '3.0.3', '3.1.0'].includes(openapiVersion)) {
      warnings.push({ message: `OpenAPI version ${openapiVersion} may not be fully supported`, severity: 'warning' });
    }

    // Info object validation
    if (!parsedSpec.info) {
      errors.push({ message: 'Missing info object', severity: 'error' });
    } else {
      if (!parsedSpec.info.title) {
        warnings.push({ message: 'info.title is recommended', severity: 'warning' });
      }
      if (!parsedSpec.info.version) {
        errors.push({ message: 'info.version is required', severity: 'error' });
      }
    }

    // Paths validation
    if (!parsedSpec.paths || Object.keys(parsedSpec.paths).length === 0) {
      warnings.push({ message: 'No paths defined', severity: 'warning' });
    } else {
      // Check each path
      for (const [path, methods] of Object.entries(parsedSpec.paths)) {
        if (!path.startsWith('/')) {
          errors.push({ message: `Path "${path}" must start with "/"`, severity: 'error' });
        }

        for (const [method, operation] of Object.entries(methods)) {
          const validMethods = ['get', 'post', 'put', 'delete', 'patch', 'head', 'options'];
          if (!validMethods.includes(method.toLowerCase())) continue;

          if (!operation.operationId && !operation.summary) {
            warnings.push({
              message: `${method.toUpperCase()} ${path} missing operationId or summary`,
              severity: 'warning'
            });
          }

          if (!operation.responses) {
            errors.push({
              message: `${method.toUpperCase()} ${path} missing responses`,
              severity: 'error'
            });
          }
        }
      }
    }

    // Security schemes validation
    if (parsedSpec.components?.securitySchemes || parsedSpec.securityDefinitions) {
      const schemes = parsedSpec.components?.securitySchemes || parsedSpec.securityDefinitions;
      for (const [name, scheme] of Object.entries(schemes)) {
        if (!scheme.type) {
          errors.push({ message: `Security scheme "${name}" missing type`, severity: 'error' });
        }
      }
    }

    return res.status(200).json({
      valid: errors.length === 0,
      errors,
      warnings,
      summary: {
        total: errors.length + warnings.length,
        errors: errors.length,
        warnings: warnings.length
      },
      stats: {
        paths: Object.keys(parsedSpec.paths || {}).length,
        operations: Object.values(parsedSpec.paths || {}).reduce((acc, methods) =>
          acc + Object.keys(methods).filter(m => ['get','post','put','delete','patch'].includes(m)).length, 0),
        schemas: Object.keys(parsedSpec.components?.schemas || {}).length
      }
    });

  } catch (error) {
    return res.status(500).json({
      valid: false,
      errors: [{ message: 'Internal validation error: ' + error.message, severity: 'error' }],
      summary: { total: 1, errors: 1, warnings: 0 }
    });
  }
};
