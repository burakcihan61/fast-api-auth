# Commit Rules

## Commit Message Format

Her commit mesajı **header**, **body** ve **footer** içermelidir:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Header

Header **zorunludur** ve `<type>(<scope>): <subject>` formatındadır.

#### Type (Zorunlu)

Commit tipini belirtir:

- **feat**: Yeni özellik ekleme
- **fix**: Hata düzeltme
- **docs**: Dokümantasyon değişiklikleri
- **style**: Kod formatı (boşluk, noktalama, vb. - işlevselliği değiştirmeyen)
- **refactor**: Kod yeniden yapılandırma (ne yeni özellik ne de hata düzeltme)
- **perf**: Performans iyileştirme
- **test**: Test ekleme veya düzeltme
- **chore**: Build, CI/CD veya yardımcı araç değişiklikleri
- **revert**: Önceki commit'i geri alma
- **security**: Güvenlik iyileştirmeleri

#### Scope (Opsiyonel)

Değişikliğin hangi modülü etkilediğini belirtir:

- **auth**: Authentication (login, register, logout)
- **user**: User management
- **api**: API endpoints
- **db**: Database models, migrations
- **cache**: Redis cache functions
- **config**: Configuration files
- **docker**: Docker, docker-compose
- **deps**: Dependencies
- **ci**: CI/CD pipeline
- **tests**: Test files

#### Subject (Zorunlu)

- İngilizce yazılmalı
- İmperative mood kullanılmalı ("add" not "added" or "adds")
- İlk harf küçük
- Sonunda nokta yok
- Maksimum 72 karakter

**Örnekler:**
```
feat(auth): add logout endpoint with token blacklist
fix(user): resolve password validation error
docs(readme): update installation instructions
```

### Body (Opsiyonel)

- Değişikliğin **ne** yaptığını ve **neden** yapıldığını açıkla
- **Nasıl** yaptığını açıklama (kod kendini açıklamalı)
- Her satır maksimum 72 karakter

### Footer (Opsiyonel)

**Breaking Changes:**
```
BREAKING CHANGE: JWT token format changed, requires re-login
```

**Issue References:**
```
Closes #123
Fixes #456, #789
```

---

## Commit Örnekleri

### ✅ İyi Commit

```
feat(auth): add JWT token blacklist for logout

Implement Redis-based token blacklist to invalidate tokens on logout.
Tokens are stored in Redis with 30-minute TTL matching token expiration.

- Add blacklist_token() function to cache.py
- Add is_token_blacklisted() check in authentication
- Create POST /api/v1/auth/logout endpoint

Closes #42
```

### ✅ Basit Commit

```
fix(user): correct email validation regex
```

### ❌ Kötü Commit

```
updated stuff
```

```
fix bug
```

```
WIP
```

---

## Commit Kuralları

### 1. Atomic Commits

- **Her commit bir mantıksal değişiklik içermeli**
- Birden fazla özellik/düzeltme tek commit'te olmamalı
- Tek bir özellik birden fazla commit'e bölünmemeli

**Kötü:**
```
feat: add login, register, logout and fix database bug
```

**İyi:**
```
feat(auth): add login endpoint
feat(auth): add register endpoint
feat(auth): add logout endpoint with token blacklist
fix(db): resolve connection pool timeout
```

### 2. Test Edilmiş Commits

- Her commit çalışan kod içermeli
- Testler başarılı olmalı
- Build hatasız tamamlanmalı

### 3. Anlamlı Commit Messages

- Değişikliği net açıkla
- Gelecekte anlaşılır olmalı
- "WIP", "temp", "fix" gibi genel ifadeler kullanma

### 4. Commit Sırası

1. feat: Yeni özellikler
2. fix: Hata düzeltmeleri
3. refactor: Kod iyileştirmeleri
4. docs: Dokümantasyon
5. test: Testler
6. chore: Diğer değişiklikler

---

## Branch Naming Convention

### Format

```
<type>/<short-description>
```

### Types

- **feature/** - Yeni özellik
- **bugfix/** - Hata düzeltme
- **hotfix/** - Acil production düzeltmesi
- **refactor/** - Kod yeniden yapılandırma
- **docs/** - Dokümantasyon
- **test/** - Test ekleme/düzeltme

### Örnekler

```
feature/user-profile
feature/jwt-refresh-token
bugfix/email-validation
hotfix/security-vulnerability
refactor/user-crud-methods
docs/api-documentation
test/auth-endpoints
```

---

## Pull Request Template

```markdown
## Description
<!-- Değişikliğin kısa açıklaması -->

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes Made
<!-- Yapılan değişikliklerin listesi -->
- 
- 

## Testing
<!-- Nasıl test edildi? -->
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests added/updated
- [ ] All tests pass

## Related Issues
<!-- Issue numaralarını belirt -->
Closes #
```

---

## Pre-commit Checklist

Commit yapmadan önce:

- [ ] Kod çalışıyor mu?
- [ ] Testler geçiyor mu?
- [ ] Linter hataları var mı?
- [ ] Type checking geçiyor mu?
- [ ] Dokümantasyon güncellendi mi?
- [ ] Commit mesajı kurallara uygun mu?
- [ ] Gereksiz dosyalar staged'da değil mi?

---

## Git Workflow

### 1. Feature Geliştirme

```bash
# 1. Ana branch'ten yeni branch oluştur
git checkout main
git pull origin main
git checkout -b feature/new-feature

# 2. Değişiklikleri yap
# ... kod yaz ...

# 3. Stage ve commit
git add .
git commit -m "feat(scope): description"

# 4. Push
git push origin feature/new-feature

# 5. Pull Request aç
# GitHub/GitLab'da PR oluştur
```

### 2. Hotfix

```bash
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug

# Fix yap
git add .
git commit -m "fix(scope): resolve critical bug"

git push origin hotfix/critical-bug
# PR oluştur ve hemen merge et
```

---

## Commit Signature

GPG ile commit imzalama (önerilen):

```bash
# GPG key oluştur
gpg --gen-key

# Git'e key'i tanıt
git config --global user.signingkey <KEY_ID>

# Otomatik imzalama
git config --global commit.gpgsign true

# İmzalı commit
git commit -S -m "feat(auth): add 2FA support"
```

---

## Örnek Commit Geçmişi

```
* feat(auth): add logout endpoint with token blacklist
* feat(auth): implement JWT refresh token
* fix(user): resolve email uniqueness validation
* refactor(api): improve error handling middleware
* test(auth): add integration tests for login flow
* docs(readme): update API documentation
* chore(deps): update fastapi to 0.115.0
* ci: add GitHub Actions workflow
```

---

## Forbidden Patterns

❌ **Yapılmaması Gerekenler:**

```bash
# Çok genel mesajlar
git commit -m "update"
git commit -m "fix"
git commit -m "changes"

# WIP commits (rebase/squash yapılmalı)
git commit -m "WIP"
git commit -m "temp"

# Birden fazla concern
git commit -m "add feature X and fix bug Y and update docs"

# Büyük binary dosyalar
git add *.zip
git add *.exe
git add large-dataset.csv
```

---

## Tools

### Pre-commit Hooks

`.pre-commit-config.yaml` dosyası zaten yapılandırılmış:

```bash
# Pre-commit hooks'u kur
pre-commit install

# Manuel çalıştır
pre-commit run --all-files
```

### Commitlint

Commit mesajlarını otomatik kontrol et:

```bash
npm install -g @commitlint/cli @commitlint/config-conventional

# .commitlintrc.json
{
  "extends": ["@commitlint/config-conventional"]
}
```

---

## Best Practices

1. **Sık commit yap** - Küçük, anlamlı commits
2. **Pull önce** - Push etmeden önce her zaman pull yap
3. **Review yap** - `git diff` ile değişiklikleri kontrol et
4. **Rebase kullan** - Temiz geçmiş için rebase, public branch'lerde merge
5. **Force push yapma** - Shared branch'lerde `-f` kullanma
6. **Secrets commit etme** - `.env`, keys, passwords asla commit edilmemeli

---

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Best Practices](https://git-scm.com/book/en/v2)
- [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)
