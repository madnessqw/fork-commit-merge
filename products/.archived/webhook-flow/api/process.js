/**
 * WebhookFlow — Webhook Orchestrator
 * Receives webhook payloads, applies routing rules, transforms, and forwards.
 */

module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, X-License-Key");

  if (req.method === "OPTIONS") return res.status(200).json({ ok: true });
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  try {
    const { payload, rules } = req.body || {};

    if (!payload) {
      return res.status(400).json({
        error: "Missing 'payload' field. Send the webhook data you want to process.",
        example: {
          payload: { event: "order.created", data: { id: 123, total: 49.99 } },
          rules: []
        }
      });
    }

    const appliedRules = Array.isArray(rules) ? rules : [];
    const results = [];

    for (const rule of appliedRules) {
      const { condition, transform, destination } = rule;
      let matched = true;

      // Evaluate condition
      if (condition) {
        const { field, operator, value } = condition;
        const actualValue = getNestedValue(payload, field);
        matched = evaluateCondition(actualValue, operator, value);
      }

      if (!matched) {
        results.push({ rule: rule.name || "unnamed", matched: false, forwarded: false });
        continue;
      }

      // Apply transformation if any
      let output = transform ? applyTransform(payload, transform) : payload;

      results.push({
        rule: rule.name || "unnamed",
        matched: true,
        transformed: output,
        destination: destination || null,
        forwarded: !!destination
      });
    }

    // If no rules, echo with metadata
    if (appliedRules.length === 0) {
      return res.status(200).json({
        ok: true,
        processed: true,
        payload,
        rulesEvaluated: 0,
        results: [],
        message: "Payload received. Add routing rules in the premium version to enable orchestration.",
        metadata: {
          receivedAt: new Date().toISOString(),
          payloadSize: JSON.stringify(payload).length,
          topKeys: Object.keys(payload)
        }
      });
    }

    return res.status(200).json({
      ok: true,
      processed: true,
      rulesEvaluated: results.length,
      matched: results.filter(r => r.matched).length,
      forwarded: results.filter(r => r.forwarded).length,
      results,
      metadata: {
        receivedAt: new Date().toISOString(),
        payloadSize: JSON.stringify(payload).length
      }
    });

  } catch (error) {
    return res.status(500).json({ error: "Processing failed", message: error.message });
  }
};

function getNestedValue(obj, path) {
  if (!path) return undefined;
  return path.split(".").reduce((acc, key) => acc && acc[key], obj);
}

function evaluateCondition(actual, operator, expected) {
  switch (operator) {
    case "equals": return actual === expected;
    case "not_equals": return actual !== expected;
    case "contains": return String(actual || "").includes(String(expected));
    case "starts_with": return String(actual || "").startsWith(String(expected));
    case "exists": return actual !== undefined && actual !== null;
    case "greater_than": return Number(actual) > Number(expected);
    case "less_than": return Number(actual) < Number(expected);
    default: return actual === expected;
  }
}

function applyTransform(payload, transform) {
  if (transform.type === "pick") {
    const result = {};
    for (const key of transform.keys || []) {
      result[key] = getNestedValue(payload, key);
    }
    return result;
  }
  if (transform.type === "add_fields") {
    return { ...payload, ...transform.fields };
  }
  if (transform.type === "rename") {
    const result = { ...payload };
    for (const [from, to] of Object.entries(transform.mapping || {})) {
      const val = getNestedValue(result, from);
      if (val !== undefined) {
        result[to] = val;
        deleteNestedValue(result, from);
      }
    }
    return result;
  }
  return payload;
}

function deleteNestedValue(obj, path) {
  const parts = path.split(".");
  const last = parts.pop();
  const parent = parts.reduce((acc, key) => acc && acc[key], obj);
  if (parent && last) delete parent[last];
}
