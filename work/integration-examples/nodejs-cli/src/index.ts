#!/usr/bin/env node

import { Command } from 'commander';
import inquirer from 'inquirer';
import chalk from 'chalk';
import ora from 'ora';
import { PrivacySDK, PrivacyConfig } from '@privacylayer/sdk';
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

const program = new Command();
const CONFIG_PATH = join(process.env.HOME || '.', '.privacyrc.json');

function loadConfig(): PrivacyConfig {
  if (existsSync(CONFIG_PATH)) {
    return JSON.parse(readFileSync(CONFIG_PATH, 'utf-8'));
  }
  return {
    network: 'testnet',
    defaultPrivacyLevel: 'medium'
  };
}

const sdk = new PrivacySDK(loadConfig());

program
  .name('privacy-cli')
  .description('PrivacyLayer CLI - Private blockchain transactions')
  .version('1.0.0');

program
  .command('deposit')
  .description('Make a private deposit')
  .option('-a, --amount <amount>', 'Amount to deposit')
  .option('-p, --privacy <level>', 'Privacy level (low/medium/high)', 'medium')
  .option('-r, --recipient <address>', 'Recipient address')
  .action(async (options) => {
    let { amount, privacy, recipient } = options;

    if (!amount) {
      const answer = await inquirer.prompt([{
        type: 'input',
        name: 'amount',
        message: 'Amount (ETH):',
        validate: (v) => parseFloat(v) > 0 || 'Amount must be positive'
      }]);
      amount = answer.amount;
    }

    if (!recipient) {
      const answer = await inquirer.prompt([{
        type: 'input',
        name: 'recipient',
        message: 'Recipient address:',
        validate: (v) => v.startsWith('0x') || 'Invalid address'
      }]);
      recipient = answer.recipient;
    }

    const spinner = ora('Processing private deposit...').start();

    try {
      const result = await sdk.deposit({
        amount,
        privacyLevel: privacy,
        recipient
      });
      spinner.succeed(chalk.green(`Deposit successful! TX: ${result.hash}`));
    } catch (error) {
      spinner.fail(chalk.red(`Deposit failed: ${error instanceof Error ? error.message : error}`));
      process.exit(1);
    }
  });

program
  .command('balance')
  .description('Check private balance')
  .option('--json', 'Output as JSON')
  .action(async (options) => {
    try {
      const balance = await sdk.getBalance();
      if (options.json) {
        console.log(JSON.stringify({ balance }, null, 2));
      } else {
        console.log(chalk.blue(`Private Balance: ${balance} ETH`));
      }
    } catch (error) {
      console.error(chalk.red(`Error: ${error instanceof Error ? error.message : error}`));
      process.exit(1);
    }
  });

program
  .command('history')
  .description('Show transaction history')
  .option('-l, --limit <n>', 'Number of transactions', '10')
  .option('--format <fmt>', 'Output format (table/json/csv)', 'table')
  .action(async (options) => {
    const spinner = ora('Fetching history...').start();
    try {
      const txs = await sdk.getHistory({ limit: parseInt(options.limit) });
      spinner.stop();
      
      if (options.format === 'json') {
        console.log(JSON.stringify(txs, null, 2));
      } else if (options.format === 'csv') {
        console.log('hash,type,amount,privacyLevel,status');
        txs.forEach(tx => console.log(`${tx.hash},${tx.type},${tx.amount},${tx.privacyLevel},${tx.status}`));
      } else {
        console.log(chalk.bold('\nTransaction History:'));
        console.log('-'.repeat(80));
        txs.forEach(tx => {
          const status = tx.status === 'confirmed' ? chalk.green('✓') : 
                        tx.status === 'pending' ? chalk.yellow('⏳') : chalk.red('✗');
          console.log(`${status} ${tx.type.toUpperCase().padEnd(10)} ${tx.amount.padEnd(10)} ETH  ${tx.privacyLevel.padEnd(8)}  ${tx.hash.slice(0, 20)}...`);
        });
      }
    } catch (error) {
      spinner.fail(chalk.red(`Failed: ${error instanceof Error ? error.message : error}`));
    }
  });

program.parse();
