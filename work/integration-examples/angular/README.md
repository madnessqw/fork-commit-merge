# PrivacyLayer Angular Integration Example

An Angular application demonstrating PrivacyLayer SDK integration with RxJS state management.

## Features

- 🅰️ Angular 17+ with standalone components
- 🔄 RxJS-based reactive state
- 🛡️ TypeScript strict mode
- 🎨 Angular Material UI

## Quick Start

```bash
cd examples/angular
npm install
ng serve
```

## Architecture

```
src/
├── app/
│   ├── services/
│   │   └── privacy.service.ts    # SDK wrapper service
│   ├── components/
│   │   ├── deposit/
│   │   ├── withdraw/
│   │   └── history/
│   ├── models/
│   │   └── transaction.model.ts
│   └── app.config.ts
```

## Usage

```typescript
// app.component.ts
import { Component, inject } from '@angular/core';
import { PrivacyService } from './services/privacy.service';

@Component({
  selector: 'app-root',
  standalone: true,
  template: `
    <div class="container">
      <app-deposit-form />
      <app-transaction-list />
    </div>
  `
})
export class AppComponent {
  private privacy = inject(PrivacyService);
  
  constructor() {
    this.privacy.initialize({ network: 'testnet' });
  }
}
```

## Privacy Service

```typescript
@Injectable({ providedIn: 'root' })
export class PrivacyService {
  private sdk = new PrivacySDK();
  
  balance$ = new BehaviorSubject<string>('0');
  transactions$ = new BehaviorSubject<Transaction[]>([]);
  loading$ = new BehaviorSubject<boolean>(false);
  
  async deposit(params: DepositParams) {
    this.loading$.next(true);
    try {
      const result = await this.sdk.deposit(params);
      await this.refreshData();
      return result;
    } finally {
      this.loading$.next(false);
    }
  }
  
  private async refreshData() {
    this.balance$.next(await this.sdk.getBalance());
    this.transactions$.next(await this.sdk.getHistory());
  }
}
```

## Components

- `DepositComponent` — Form with privacy level selector
- `WithdrawComponent` — Withdrawal interface
- `HistoryComponent` — Transaction list with filters
- `PrivacyIndicatorComponent` — Visual privacy level badge

## License

MIT - Part of PrivacyLayer SDK Examples
