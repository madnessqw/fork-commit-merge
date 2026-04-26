import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { PrivacySDK, PrivacyConfig, DepositParams, WithdrawParams } from '@privacylayer/sdk';

export interface Transaction {
  hash: string;
  type: 'deposit' | 'withdraw';
  amount: string;
  privacyLevel: string;
  timestamp: number;
  status: 'pending' | 'confirmed' | 'failed';
}

@Injectable({ providedIn: 'root' })
export class PrivacyService {
  private sdk: PrivacySDK | null = null;
  
  balance$ = new BehaviorSubject<string>('0');
  transactions$ = new BehaviorSubject<Transaction[]>([]);
  loading$ = new BehaviorSubject<boolean>(false);
  error$ = new BehaviorSubject<string | null>(null);

  initialize(config: PrivacyConfig) {
    this.sdk = new PrivacySDK(config);
    this.refreshData();
  }

  async deposit(params: DepositParams): Promise<{ hash: string }> {
    if (!this.sdk) throw new Error('SDK not initialized');
    
    this.loading$.next(true);
    this.error$.next(null);
    
    try {
      const result = await this.sdk.deposit(params);
      await this.refreshData();
      return result;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Deposit failed';
      this.error$.next(message);
      throw err;
    } finally {
      this.loading$.next(false);
    }
  }

  async withdraw(params: WithdrawParams): Promise<{ hash: string }> {
    if (!this.sdk) throw new Error('SDK not initialized');
    
    this.loading$.next(true);
    this.error$.next(null);
    
    try {
      const result = await this.sdk.withdraw(params);
      await this.refreshData();
      return result;
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Withdrawal failed';
      this.error$.next(message);
      throw err;
    } finally {
      this.loading$.next(false);
    }
  }

  private async refreshData() {
    if (!this.sdk) return;
    
    try {
      const balance = await this.sdk.getBalance();
      const transactions = await this.sdk.getHistory();
      
      this.balance$.next(balance);
      this.transactions$.next(transactions);
    } catch (err) {
      console.error('Failed to refresh data:', err);
    }
  }

  getBalance(): Observable<string> {
    return this.balance$.asObservable();
  }

  getTransactions(): Observable<Transaction[]> {
    return this.transactions$.asObservable();
  }

  isLoading(): Observable<boolean> {
    return this.loading$.asObservable();
  }

  getError(): Observable<string | null> {
    return this.error$.asObservable();
  }
}
